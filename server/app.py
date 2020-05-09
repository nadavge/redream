import socketio
import eventlet
import threading
import Queue

ALL_ROOM = "ALL"

dreamcastQ = Queue.Queue()
current_state = {
    "connections": {
        "current": [],
        "history": []
    }
}
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/index.html': {'content_type': 'text/html', 'filename': '../client/index.html'}
})

@sio.event
def connect(sid, environ):
    print 'Connected:', sid
    sio.emit('sync_state', current_state, sid)
    sio.enter_room(sid, ALL_ROOM)

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    sio.leave_room(sid, 'all')
    print 'Disconnected: ', sid

def run_server():
    # Spawn an dreamcast middle-man thread. This is required since updates need
    # to run from eventlet's context, so that sio would work well.
    eventlet.spawn(dreamcast_rpc_thread)
    eventlet.wsgi.server(eventlet.listen(('localhost', 8000)), app)

def dreamcast_rpc_thread():
    import time
    prev_time = time.time()
    update_count = 0
    while True:
        try:
            message = dreamcastQ.get_nowait()
        except Queue.Empty:
            eventlet.sleep(0.01)
            continue

        update_count += 1
        fake_connection = {
            "src_ip": "192.168.1.100",
            "src_port": update_count,
            "dest_ip": "192.168.1.101",
            "dest_port": update_count
        }
        current_state["connections"]["current"].append(fake_connection)
        sio.emit('new_connection', fake_connection, room=ALL_ROOM)

        prev_time = time.time()

def dreamcast_simulator():
    while True:
        dreamcastQ.put_nowait("Hello World")
        import time
        time.sleep(0.2)

def main():
    # Set the server to Daemon mode so that it could be terminated with CTRL+C
    server = threading.Thread(target=run_server)
    server.daemon = True
    server.start()
    
    dreamcast_sim = threading.Thread(target=dreamcast_simulator)
    dreamcast_sim.daemon = True
    dreamcast_sim.start()

    while True:
        import time
        time.sleep(1)

if __name__ == '__main__':
    main()
