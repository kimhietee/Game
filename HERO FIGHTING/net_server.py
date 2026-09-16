import socket
import threading
import time
import random
from network import send_msg, recv_msg

HOST = '0.0.0.0'
PORT = 5555

# Shared input state — server stores latest inputs from each player
player_inputs = {
    1: {'left': False, 'right': False, 'up': False,
        'skill1': False, 'skill2': False, 'skill3': False,
        'skill4': False, 'basic': False, 'special': False},
    2: {'left': False, 'right': False, 'up': False,
        'skill1': False, 'skill2': False, 'skill3': False,
        'skill4': False, 'basic': False, 'special': False},
}
clients = {}   # player_type (1 or 2) -> socket
lock = threading.Lock()

# ── Phase 2: lobby state ──
lobby = {
    'map': None,          # chosen by host (player 1)
    'p1_hero': None,      # hero name confirmed by p1
    'p2_hero': None,      # hero name confirmed by p2
    'p1_items': [],
    'p2_items': [],
    'p1_ready': False,
    'p2_ready': False,
    'p1_opponent_hero_ready': False, # check if p1 loads the p2 successfully
    'p2_opponent_hero_ready': False,
    'p1_rematch': False,
    'p2_rematch': False,
}

# ── Phase 2: cube position authority ──
cube_states = [
    {'fall': -500, 'x': 640},   # health cube
    {'fall': -300, 'x': 640},   # mana cube
    {'fall': -700, 'x': 640},   # special cube
]

def broadcast(msg):
    # print(f"[SERVER] Broadcasting: {msg['type']} to {list(clients.keys())} players")
    for sock in list(clients.values()):
        try: send_msg(sock, msg)
        except: pass

def handle_client(conn, player_type):
    print(f"[SERVER] Player {player_type} connected.")
    # print(f"[SERVER] clients now: {list(clients.keys())}")
    try:
        while True:
            msg = recv_msg(conn)
            if msg is None:
                break


            message_type = msg.get('type')
            # print(f"[SERVER] Received '{message_type}' from Player {player_type}")
            if message_type == 'input':
                with lock:
                    player_inputs[player_type] = msg['keys']
                # Broadcast both players' latest inputs to everyone
                with lock:
                    state = {
                        'type': 'inputs',
                        'p1': dict(player_inputs[1]),
                        'p2': dict(player_inputs[2]),
                    }
                broadcast(state)

            elif message_type == 'state':
                # Host (P1) broadcasts authoritative hero state — forward to the
                # other player(s). Not echoed back to the sender.
                for pt, sock in list(clients.items()):
                    if pt != player_type:
                        try: send_msg(sock, msg)
                        except: pass

            elif message_type == 'skill_event':
                # Host (P1) announces a skill cast — forward to the other
                # player(s) so P2 can spawn the matching Attack_Display visual.
                # Same relay pattern as 'state'; not echoed back to the sender.
                for pt, sock in list(clients.items()):
                    if pt != player_type:
                        try: send_msg(sock, msg)
                        except: pass

            # ── Phase 2: lobby messages ──
            elif message_type == 'set_map':
                lobby['map'] = msg['map']
                broadcast({'type': 'map_set', 'map': msg['map']})
            elif message_type == 'hero_ready':
                lobby[f'p{player_type}_hero'] = msg['hero']
                lobby[f'p{player_type}_ready'] = True
                broadcast({'type': 'hero_confirmed', 'player': player_type, 'hero': msg['hero']})                
                if lobby['p1_ready'] and lobby['p2_ready']:
                    broadcast({'type': 'both_ready',
                               'p1_hero': lobby['p1_hero'],
                               'p2_hero': lobby['p2_hero'],
                               'map': lobby['map']})
                    lobby['p1_ready'] = False
                    lobby['p2_ready'] = False
            
            # elif message_type == 'hero_not_ready':
            #     lobby[f'p{player_type}_ready'] = False
            #     broadcast({'type': 'not_ready'})

            elif message_type == 'load_opponent_hero':
                lobby[f'p{player_type}_opponent_hero_ready'] = True
                if lobby['p1_opponent_hero_ready'] and lobby['p2_opponent_hero_ready']:
                    # Generate a shared seed so both clients produce identical initial cube X positions
                    shared_seed = random.randint(0, 2**31 - 1)
                    broadcast({'type': 'ready_to_battle', 'cube_seed': shared_seed})
                    lobby['p1_opponent_hero_ready'] = False
                    lobby['p2_opponent_hero_ready'] = False
                
            elif message_type == 'cube_reset':
                idx = msg['index']
                cube_states[idx]['fall'] = msg['fall']
                cube_states[idx]['x'] = msg['x']
                broadcast({
                    'type': 'cube_update', 
                    'index': idx, 
                    'fall': msg['fall'], 
                    'x': msg['x'],
                    'hero_hit': msg.get('hero_hit'), 
                    'bonus_type': msg.get('bonus_type'), 
                    'bonus_amount': msg.get('bonus_amount')
                })

            elif message_type == 'report_hp':
                # P1 is the authority — only accept HP reports from player 1
                if player_type == 1:
                    p1_hp = msg['p1_hp']
                    p2_hp = msg['p2_hp']
                    declared_winner = None
                    if p1_hp <= 0 and p2_hp <= 0:
                        declared_winner = 'hero1'  # draw goes to hero1 (matches existing logic)
                    elif p1_hp <= 0:
                        declared_winner = 'hero2'
                    elif p2_hp <= 0:
                        declared_winner = 'hero1'
                    if declared_winner is not None:
                        broadcast({'type': 'winner_declared', 'winner': declared_winner})

            elif message_type == 'rematch_request':
                lobby[f'p{player_type}_rematch'] = True
                broadcast({'type': 'rematch_request_received', 'player': player_type})
                if lobby['p1_rematch'] and lobby['p2_rematch']:
                    lobby['p1_rematch'] = False
                    lobby['p2_rematch'] = False
                    lobby['p1_ready'] = False
                    lobby['p2_ready'] = False
                    lobby['p1_opponent_hero_ready'] = False
                    lobby['p2_opponent_hero_ready'] = False
                    broadcast({'type': 'rematch_confirmed'})

    except (ConnectionResetError, ConnectionAbortedError):
        print('[SERVER] Connection error!')
    finally:
        with lock:
            clients.pop(player_type, None)
            print(f"[SERVER] Player {player_type} disconnected.")
            # print(f"[SERVER] clients now: {list(clients.keys())}")
        conn.close()
        for pt, sock in clients.items():
            try:
                send_msg(sock, {'type': 'opponent_left'})
            except:
                pass

def accept_loop():
    while True:
        try:
            conn, addr = server.accept()
        except OSError:
            break  # server socket closed (shutdown)
        with lock:
            # Assign the lowest free slot so a player who left can be replaced
            # without waiting for the other player to disconnect too.
            pt = next((s for s in (1, 2) if s not in clients), None)
            if pt is None:
                conn.close()
                continue
            clients[pt] = conn
            both_connected = len(clients) == 2
        send_msg(conn, {'type': 'welcome', 'your_player_type': pt})
        thread = threading.Thread(target=handle_client, args=(conn, pt), daemon=True)
        thread.start()
        if both_connected:
            broadcast({'type': 'start'})
            print("[SERVER] Both players connected. Game starting.")

server = None  # set by serve(); module-level so accept_loop()/broadcast() can use it


def _reset_state():
    """Clear lobby/input/cube state so an in-process host can start a fresh match."""
    for pt in (1, 2):
        player_inputs[pt] = {'left': False, 'right': False, 'up': False,
                             'skill1': False, 'skill2': False, 'skill3': False,
                             'skill4': False, 'basic': False, 'special': False}
    clients.clear()
    lobby.update({'map': None, 'p1_hero': None, 'p2_hero': None,
                  'p1_ready': False, 'p2_ready': False,
                  'p1_opponent_hero_ready': False, 'p2_opponent_hero_ready': False,
                  'p1_rematch': False, 'p2_rematch': False})


def serve(host=HOST, port=PORT):
    """Bind, listen and run the accept loop (blocking). Used both as a standalone
    process and inside a background thread when the host runs the server in-process."""
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()
    # print(f"[SERVER] Listening on port {port}...")
    start_udp_broadcast()
    accept_loop()


_server_thread = None  # the in-process accept-loop thread, if hosting
_udp_broadcaster_thread = None
_udp_broadcaster_running = False
UDP_PORT = 5556

def _get_local_ip():
    """Return the single LAN IP the OS would use to reach the internet.
    Used as a fallback when full interface enumeration fails."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'
    finally:
        s.close()


def _get_all_broadcast_targets():
    """Return a list of (local_ip, directed_broadcast) for every real IPv4
    interface on this machine.

    Why this matters: an *unbound* UDP socket lets the OS pick which NIC to
    send on.  On machines with a VPN adapter (Radmin, Hamachi, ZeroTier …)
    that choice can land on the wrong interface and the beacon never reaches
    the real LAN.  Binding one socket *per interface* forces each send out the
    correct NIC, and the directed broadcast (e.g. 192.168.0.255) is the
    address that home routers actually propagate — unlike 255.255.255.255
    which many routers quietly drop.

    Assumes /24 subnet for the directed-broadcast calculation, which is correct
    for virtually every home and small-office network."""
    addrs = []

    # Method 1: gethostbyname_ex — fast, stdlib, works on Windows and Linux
    try:
        _, _, gethostname_addrs = socket.gethostbyname_ex(socket.gethostname())
        addrs.extend(gethostname_addrs)
    except Exception:
        pass

    # Method 2: routing-table probe — catches the "primary" interface even if
    # gethostbyname_ex misses it (e.g. when hostname resolves to 127.0.x.x)
    fallback = _get_local_ip()
    if fallback not in addrs:
        addrs.append(fallback)

    seen = set()
    targets = []
    for ip in addrs:
        if ip.startswith('127.') or ip in seen:
            continue
        seen.add(ip)
        # /24 directed broadcast: replace last octet with 255
        prefix = ip.rsplit('.', 1)[0]
        targets.append((ip, prefix + '.255'))

    return targets

_bound_port = PORT  # the TCP port the in-process server actually bound to
_room_name = ''     # optional human-readable room name shown to joiners


def get_server_port():
    """Return the TCP port the in-process host is currently listening on."""
    return _bound_port


def set_room_name(name):
    """Set the human-readable room name advertised in the UDP beacon."""
    global _room_name
    _room_name = (name or '').strip()


def _encode_room_name(name):
    """Make the room name safe to embed in the ':'-delimited beacon: percent-encode
    so a name containing ':' (or spaces) can't break parsing on the client."""
    from urllib.parse import quote
    return quote(name or '', safe='')


def _udp_broadcast_loop():
    """Broadcast a discovery beacon on every real LAN interface.

    One UDP socket is created *and bound* to each interface so the OS is
    forced to transmit out that specific NIC instead of guessing.  From each
    socket we send to both the /24 directed broadcast (e.g. 192.168.0.255)
    and 255.255.255.255 — the first is what home routers propagate; the second
    is a belt-and-suspenders fallback.  The beacon embeds the interface's own
    IP so joiners know which address to TCP-connect to.

    Message format (unchanged, backward-compatible with existing client):
        HERO_FIGHTING_LOBBY:<ip>:<port>:<url-encoded room name>
    """
    global _udp_broadcaster_running
    encoded_name = _encode_room_name(_room_name)

    # --- Build one (socket, beacon_bytes, directed_bcast) per interface ---
    targets = _get_all_broadcast_targets()
    if not targets:
        local_ip = _get_local_ip()
        prefix = local_ip.rsplit('.', 1)[0]
        targets = [(local_ip, prefix + '.255')]   # should never happen

    iface_sockets = []   # list of (socket, beacon_bytes, directed_bcast_str)
    summary_parts  = []

    for local_ip, directed_bcast in targets:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        try:
            s.bind((local_ip, 0))   # pin this socket to the specific NIC
        except Exception as e:
            print(f"[SERVER UDP] Cannot bind to {local_ip}: {e} — skipping")
            s.close()
            continue
        beacon = (
            f"HERO_FIGHTING_LOBBY:{local_ip}:{_bound_port}:{encoded_name}"
        ).encode('utf-8')
        iface_sockets.append((s, beacon, directed_bcast))
        summary_parts.append(f"{local_ip} → [{directed_bcast}, 255.255.255.255]")

    if not iface_sockets:
        # absolute last resort — old unbound single-socket behaviour
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        local_ip = _get_local_ip()
        beacon = (
            f"HERO_FIGHTING_LOBBY:{local_ip}:{_bound_port}:{encoded_name}"
        ).encode('utf-8')
        iface_sockets.append((s, beacon, '255.255.255.255'))
        summary_parts.append(f"{local_ip} → [255.255.255.255] (fallback)")

    print(f"[SERVER UDP] Broadcasting on interfaces: {', '.join(summary_parts)}")

    # --- Broadcast loop ---
    while _udp_broadcaster_running:
        for s, beacon, directed_bcast in iface_sockets:
            for dest in (directed_bcast, '255.255.255.255'):
                try:
                    s.sendto(beacon, (dest, UDP_PORT))
                except Exception:
                    pass
        time.sleep(1.5)

    for s, _, _ in iface_sockets:
        try:
            s.close()
        except Exception:
            pass

def start_udp_broadcast():
    global _udp_broadcaster_thread, _udp_broadcaster_running
    if _udp_broadcaster_running:
        return
    _udp_broadcaster_running = True
    _udp_broadcaster_thread = threading.Thread(target=_udp_broadcast_loop, daemon=True)
    _udp_broadcaster_thread.start()

def stop_udp_broadcast():
    global _udp_broadcaster_running, _udp_broadcaster_thread
    _udp_broadcaster_running = False
    _udp_broadcaster_thread = None

def stop_server():
    """Stop the in-process server, closing sockets and stopping UDP broadcasting."""
    global server, _server_thread
    # print("[SERVER] Stopping server...")
    stop_udp_broadcast()
    if server is not None:
        try:
            server.close()
        except Exception as e:
            print(f"[SERVER] Error closing socket: {e}")
        server = None
    with lock:
        for pt, sock in list(clients.items()):
            try:
                sock.close()
            except:
                pass
        clients.clear()
    _server_thread = None
    # print("[SERVER] Server stopped.")


def start_background_server(host=HOST, port=PORT, max_port=PORT + 20, room_name=''):
    """Host-in-process: bind/listen here then run the accept loop on a daemon thread.
    Idempotent within a process — if we're already hosting, the existing server is
    reused (its state is reset for a fresh match) rather than binding a second time.

    To let several hosts coexist on the same machine/LAN, if `port` is already
    taken we scan upward (port, port+1, ... up to max_port) for a free one.

    `room_name` is an optional human-readable label advertised to joiners.

    Returns (thread, bound_port), or (None, None) if no free port was found."""
    global server, _server_thread, _bound_port
    print('start server', 'host: ', host, ' port: ', port)
    _reset_state()
    set_room_name(room_name)
    if _server_thread is not None and _server_thread.is_alive():
        start_udp_broadcast()  # Ensure broadcasting is active
        return _server_thread, _bound_port  # already hosting in this process; reuse it

    s = None
    bound_port = None
    for candidate in range(port, max_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((host, candidate))
            bound_port = candidate
            break
        except OSError:
            s.close()
            s = None
            continue
    if s is None:
        return None, None

    s.listen()
    server = s
    _bound_port = bound_port
    # print(f"[SERVER] Listening on port {bound_port} (in-process host)...")
    start_udp_broadcast()
    _server_thread = threading.Thread(target=accept_loop, daemon=True)
    _server_thread.start()
    return _server_thread, bound_port


if __name__ == '__main__':
    try:
        serve()
    except KeyboardInterrupt:
        print("[SERVER] Shutting down.")
        stop_server()