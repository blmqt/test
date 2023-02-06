from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import sys, json, urllib.request, urllib.error, urllib.parse

def send_message(settings):
    print("DEBUG Sending message with settings %s" % settings, file=sys.stderr)
    room = settings.get('room')
    auth_token = settings.get('auth_token')
    base_url = settings.get('base_url').rstrip('/')
    fmt = settings.get('format', 'text')
    print("INFO Sending message to hipchat room=%s with format=%s" % (room, fmt), file=sys.stderr)
    url = "%s/room/%s/notification?auth_token=%s" % (
        base_url, urllib.parse.quote(room), urllib.parse.quote(auth_token)
    )
    body = json.dumps(dict(
        message=settings.get('message'),
        message_format=fmt,
        color=settings.get('color', "green")
    ))
    print('DEBUG Calling url="%s" with body=%s' % (url, body), file=sys.stderr)
    req = urllib.request.Request(url, body, {"Content-Type": "application/json"})
    try:
        res = urllib.request.urlopen(req)
        body = res.read()
        print("INFO HipChat server responded with HTTP status=%d" % res.code, file=sys.stderr)
        print("DEBUG HipChat server response: %s" % json.dumps(body), file=sys.stderr)
        return 200 <= res.code < 300
    except urllib.error.HTTPError as e:
        print("ERROR Error sending message: %s" % e, file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        payload = json.loads(sys.stdin.read())
        if not send_message(payload.get('configuration')):
            print("FATAL Failed trying to send room notification", file=sys.stderr)
            sys.exit(2)
        else:
            print("INFO Room notification successfully sent", file=sys.stderr)
    else:
        print("FATAL Unsupported execution mode (expected --execute flag)", file=sys.stderr)
        sys.exit(1)
