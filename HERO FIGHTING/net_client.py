import socket
import threading
import time
from network import send_msg, recv_msg

class NetClient:
    """
    Manages the socket connection for one player.
    The game loop calls send_input() every frame.
    The latest inputs for both players are always available
    in self.p1_keys and self.p2_keys.
    """
    def __init__(self, host, port=5555):
        self.host = host
        self.port = port
        self.sock = None
        self.my_player_type = None
        self.phase = 'connecting'   # connecting -> lobby -> playing -> disconnected
        self.p1_keys = {}
        self.p2_keys = {}
        self._lock = threading.Lock()
        self._running = False
        # ── Phase 2: lobby state ──
        self.map_selected = None
        self.p1_hero = None
        self.p2_hero = None
        self.p1_items = [] # item equipped
        self.p2_items = []
        self.p1_hero_ready = False
        self.p2_hero_ready = False
        self.both_ready = False
        self.opponent_ready = False
        self.ready_to_battle = False
        # ── Phase 2: cube sync ──
        self.cube_updates = []   # list of pending cube updates: {'index':i,'fall':f,'x':x}
        self._cube_lock = threading.Lock()
        self.opponent_left = False
        self.cube_seed = None   # shared seed for deterministic initial cube X positions
        self.declared_winner = None  # set by server in LAN mode

        self.my_rematch_sent = False
        self.opponent_rematch_sent = False
        self.rematch_confirmed = False

        # ── Phase D: host-authoritative state sync (with interpolation) ──
        # Keep the last two snapshots + their arrival times so the non-host can
        # render the opponent slightly in the past and lerp between them.
        self._state_lock = threading.Lock()
        self.prev_state = None
        self.latest_state = None
        self.prev_time = 0.0
        self.latest_time = 0.0

        # ── Skill-fired events (lossless visual trigger for P2) ──
        # The host emits one event the instant a hero actually casts a skill.
        # Unlike the sampled state snapshot (which can miss a brief
        # False->True->False attacking-flag edge under jitter), every event is
        # queued and consumed exactly once by P2, so the Attack_Display visual
        # always spawns regardless of snapshot timing.
        self._skill_event_lock = threading.Lock()
        self.skill_events = []   # list of {'hero': 1|2, 'skill': 1..5}

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Disable Nagle so the 60Hz stream of tiny input/state packets is sent
        # immediately instead of being batched (a major source of stutter).
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.connect((self.host, self.port))
        welcome = recv_msg(self.sock)
        if welcome is None:
            raise ConnectionError("No welcome message from server.")
        self.my_player_type = welcome['your_player_type']
        self._running = True
        thread = threading.Thread(target=self._recv_loop, daemon=True)
        thread.start()
        print(f"[CLIENT] Connected as Player {self.my_player_type}")

    def send_input(self, keys: dict):
        """Call every frame with a dict of booleans for this player's keys."""
        if self.sock and self._running:
            try:
                send_msg(self.sock, {'type': 'input', 'keys': keys})
                # print(keys)
            except:
                self._running = False
                self.phase = 'disconnected'

    def get_inputs(self):
        """Returns (p1_keys, p2_keys) -- latest known inputs for both players."""
        with self._lock:
            return dict(self.p1_keys), dict(self.p2_keys)
        
        

    # ── Phase 2: lobby send methods ──
    def send_map(self, map_name):
        send_msg(self.sock, {'type': 'set_map', 'map': map_name})

    def send_hero_ready(self, hero_name, item_names):
        send_msg(self.sock, {'type': 'hero_ready', 'hero': hero_name, 'items': item_names or []})

    def send_load_opponent_hero_ready(self, hero_name):
        send_msg(self.sock, {'type': 'load_opponent_hero', 'hero': hero_name})

    def send_cube_reset(self, index, fall, x, hero_hit=None, bonus_type=None, bonus_amount=None):
        if self.sock and self._running:
            try:
                send_msg(self.sock, {
                    'type': 'cube_reset', 'index': index, 'fall': fall, 'x': x,
                    'hero_hit': hero_hit, 'bonus_type': bonus_type, 'bonus_amount': bonus_amount
                })
            except:
                self._running = False
                self.phase = 'disconnected'

    def send_report_hp(self, p1_hp, p2_hp):
        send_msg(self.sock, {'type': 'report_hp', 'p1_hp': p1_hp, 'p2_hp': p2_hp})

    def send_state(self, heroes_state):
        """Host (P1) only: broadcast the authoritative hero state for this tick.
        heroes_state is {'h1': {...}, 'h2': {...}}."""
        if self.sock and self._running:
            try:
                send_msg(self.sock, {'type': 'state', 'heroes': heroes_state})
            except:
                self._running = False
                self.phase = 'disconnected'

    def send_skill_event(self, hero, skill, special_active=False):
        """Host (P1) only: announce that hero (1 or 2) just fired skill id
        (1=atk1, 2=atk2, 3=atk3, 4=sp, 5=basic). Fire-once visual trigger.
        special_active is embedded at the moment of cast so P2 can spawn the
        correct visual tier without relying on the delayed state snapshot."""
        if self.sock and self._running:
            try:
                send_msg(self.sock, {
                    'type': 'skill_event',
                    'hero': hero,
                    'skill': skill,
                    'special_active': special_active,
                })
            except:
                self._running = False
                self.phase = 'disconnected'

    def pop_skill_events(self):
        """P2 only: return and clear all pending skill-fired events."""
        with self._skill_event_lock:
            events = list(self.skill_events)
            self.skill_events.clear()
            return events

    def get_states_for_render(self):
        """P2 only: returns (prev_state, latest_state, prev_time, latest_time)
        for time-based interpolation. Times are time.monotonic() seconds."""
        with self._state_lock:
            return self.prev_state, self.latest_state, self.prev_time, self.latest_time

    def send_rematch_request(self):
        self.my_rematch_sent = True
        send_msg(self.sock, {'type': 'rematch_request'})

    def pop_cube_updates(self):
        """Returns and clears pending cube updates."""
        with self._cube_lock:
            updates = list(self.cube_updates)
            self.cube_updates.clear()
            return updates

    def _recv_loop(self):
        while self._running:
            msg = recv_msg(self.sock)
            if msg is None:
                self.phase = 'disconnected'
                self._running = False
                self.opponent_left = True  # signal game loop to exit cleanly
                break
            message_type = msg.get('type')
            # print(message_type)

            if message_type == 'start':
                self.phase = 'lobby'
            elif message_type == 'inputs':
                with self._lock:
                    self.p1_keys = msg.get('p1', {})
                    self.p2_keys = msg.get('p2', {})
            elif message_type == 'opponent_left':
                if self._running:
                    self.phase = 'lobby'
                    self.opponent_left = True
            # ── Phase 2: lobby messages ──
            elif message_type == 'map_set':
                self.map_selected = msg['map']
            elif message_type == 'hero_confirmed': # not used????
                if msg['player'] != self.my_player_type:
                    self.opponent_ready = True
                    # print('opponent ready :)')

            elif message_type == 'both_ready':
                self.p1_hero = msg['p1_hero']
                self.p2_hero = msg['p2_hero']
                self.p1_items = msg.get('p1_items', [])
                self.p2_items = msg.get('p2_items', [])
                self.map_selected = msg['map']
                # print('both ready :)')
                self.both_ready = True

            # elif message_type == 'not_ready':
            #     self.both_ready = False
            #     print('not ready :)')

            elif message_type == 'ready_to_battle':
                # print('ready to battle!!!')
                self.cube_seed = msg.get('cube_seed')  # store shared seed for cube sync
                self.ready_to_battle = True

            elif message_type == 'cube_update':
                with self._cube_lock:
                    self.cube_updates.append({
                        'index': msg['index'],
                        'fall': msg['fall'],
                        'x': msg['x'],
                        'hero_hit': msg.get('hero_hit'),
                        'bonus_type': msg.get('bonus_type'),
                        'bonus_amount': msg.get('bonus_amount'),
                    })

            elif message_type == 'state':
                _now = time.monotonic()
                with self._state_lock:
                    self.prev_state = self.latest_state
                    self.prev_time = self.latest_time
                    self.latest_state = msg.get('heroes')
                    self.latest_time = _now

            elif message_type == 'skill_event':
                with self._skill_event_lock:
                    self.skill_events.append({
                        'hero': msg.get('hero'),
                        'skill': msg.get('skill'),
                        'special_active': msg.get('special_active', False),
                    })

            elif message_type == 'winner_declared':
                self.declared_winner = msg['winner']

            elif message_type == 'rematch_request_received':
                if msg['player'] != self.my_player_type:
                    self.opponent_rematch_sent = True

            elif message_type == 'rematch_confirmed':
                self.rematch_confirmed = True

    def send_disconnect(self, hero_name):
        send_msg(self.sock, {'type': 'disconnected'})

    def disconnect(self):
        
        self._running = False
        if self.sock:
            self.sock.close()


_udp_listener_thread = None
_udp_listener_running = False
discovered_servers = {}
discovered_servers_lock = threading.Lock()
UDP_PORT = 5556

def _udp_listen_loop():
    global _udp_listener_running
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(('', UDP_PORT))
    except Exception as e:
        print(f"[CLIENT UDP] Failed to bind to UDP port {UDP_PORT}: {e}")
        sock.close()
        return

    sock.settimeout(1.0)
    while _udp_listener_running:
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode('utf-8')
            if msg.startswith("HERO_FIGHTING_LOBBY:"):
                parts = msg.split(':')
                if len(parts) >= 3:
                    ip = parts[1]
                    try:
                        port = int(parts[2])
                    except (ValueError, IndexError):
                        port = 5555
                    # Optional 4th field: a percent-encoded human-readable room
                    # name. Older hosts omit it, so fall back to a blank name.
                    room_name = ''
                    if len(parts) >= 4 and parts[3]:
                        from urllib.parse import unquote
                        room_name = unquote(parts[3])
                    # Key by ip:port so two hosts on the same machine (different
                    # ports) show up as two distinct rooms instead of colliding.
                    key = f"{ip}:{port}"
                    server_name = room_name if room_name else f"My Room"
                    with discovered_servers_lock:
                        discovered_servers[key] = (server_name, ip, port, time.time())
        except socket.timeout:
            pass
        except Exception:
            break
    sock.close()

def start_lan_scanning():
    global _udp_listener_thread, _udp_listener_running, discovered_servers
    with discovered_servers_lock:
        discovered_servers.clear()
    if _udp_listener_running:
        return
    _udp_listener_running = True
    _udp_listener_thread = threading.Thread(target=_udp_listen_loop, daemon=True)
    _udp_listener_thread.start()

def stop_lan_scanning():
    global _udp_listener_running, _udp_listener_thread
    _udp_listener_running = False
    _udp_listener_thread = None

def get_active_servers():
    """Return {key: (server_name, ip, port)} for hosts seen in the last 5s,
    where key is 'ip:port'."""
    now = time.time()
    with discovered_servers_lock:
        for key in list(discovered_servers.keys()):
            name, ip, port, last_seen = discovered_servers[key]
            if now - last_seen > 5.0:
                discovered_servers.pop(key)
        return {key: (name, ip, port) for key, (name, ip, port, _ts) in discovered_servers.items()}
