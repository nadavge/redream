import socketio
import eventlet
import threading

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': '../client/index.html'}
})
# TODO: dreamcast has one state. Make all clients participants in a room, and
#       send all updates to everyone once their state was "synced"
last_sid = None

@sio.event
def connect(sid, environ):
    global last_sid
    sio.emit('message_sync', ["abc", "cde"], sid)
    last_sid = sid

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

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
        if last_sid:
            update_count += 1
            sio.emit('message_update', ["Update #{}".format(update_count)], last_sid)
        prev_time = time.time()
        eventlet.sleep(1)

def main():
    server = threading.Thread(target=run_server)
    # Set the server to Daemon mode so that it could be terminated with CTRL+C
    server.daemon = True
    server.start()

    while True:
        import time
        time.sleep(1)

if __name__ == '__main__':
    main()
