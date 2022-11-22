from zmq.asyncio import Context, ZMQEventLoop
import zmq
from sjautils.string import before,after, split_once
import json

def ps_label(kind, kind_id=None):
    return f'{kind}:{kind_id}' if kind_id else f'{kind}'

def decode_label(label):
    kind = before(label, ':')
    kind_id = after(label, ':')
    return [kind, kind_id]

def encode_data(data):
    return json.dumps(data)

def decode_data(data):
    return json.loads(data)

def ps_encode(kind, data, kind_id=None):
    return f'{ps_label(kind, kind_id)}::{encode_data(data)}'

def ps_decode(msg):
    k_info, data = split_once(msg, '::')
    kind, kind_id = ps_parse_label(k_info)
    return kind, kind_id, decode_data(data)

class Publish:
    def __init__(self, port, type, context=None, multi=False):
        self._multi = multi
        self._socket_type = zmq.XPUB if multi else zmq.PUB
        self._addr = f'{type}://*:{port}'
        self._context = context or Context()
        self._socket = None

    @property
    def socket(self):
        if not self._socket:
            self._socket = self._context.socket(self._socket_type)
            self._socket.connect(self._addr)
        return self._socket

    def publish(self, kind, data, kind_id=None):
        # TODO add proper multi handling if different
        msg = ps_encode(kind, data, kind_id)
        self.socket.send(msg)

class Subscribe:
    def __init__(self, port, type, *filters, ip=None, context=None, multi=False):
        self._multi = multi
        self._filters = filters
        if not multi:
            assert ip, f'IP address of pub required if not multi-published'
        self._socket_type = zmq.XSUB if multi else zmq.SUB
        self._addr = f'{type}://*:{port}' if multi else f'{type}://{ip}:{port}'
        self._context = context or Context()
        self._socket = None

    @property
    def socket(self):
        if not self._socket:
            self._socket = self._context.socket(self._socket_type)
            for filter in self._filters: \
                    self._socket.setsockopt(zmq.SUBSCRIBE, filter)

            self._socket.connect(self._addr)
        return self._socket

    async def receive(self):
        if self._multi:
            msg = self._socket.receive_multipart()
            kind, kind_id = decode_label(msg[0])
            return kind, kind_id, decode_data(msg[1])
        else:
            msg = await self._socket.recv()
            return ps_decode(msg)

    async def subscription_loop(self, process_fn):
        while True:
            kind, kind_id, data = await self.receive()
            await process_fn(kind, kind_id, data)

class Server:
    def __init__(self, port, context=None, type='tcp'):
        self._context = context or Context()
        self._addr = f'{type}://*:{port}'
        self._socket = None

    @property
    def socket(self):
        if not self._socket:
            self._socket = self._context.socket(zmq.REP)
            self._socket.connect(self._addr)
        return self._socket

    def reply(self, data):
        self._socket.send(encode_data(data))

    async def receive(self):
        msg = await(self._socket.recv())
        return decode_data(msg)


class Client:
    def __init__(self, port, ip, context=None, type='tcp'):
        self._context = context or Context()
        self._addr = f'{type}://{ip}:{port}'
        self._socket = None

    @property
    def socket(self):
        if not self._socket:
            self._socket = self._context.socket(zmq.REQ)
            self._socket.connect(self._addr)
        return self._socket

    def send(self, data):
        self._socket.send(encode_data(data))

    async def receive(self):
        msg = await(self._socket.recv())
        return decode_data(msg)

"""
First try to see if tenting makes any real difference to me or not.
So far I just don't seee that it is that much different. If anything I feel
a bit more strain from the unaccustomed position.  I would estimate that the book
I am using gives perhaps a 10 degree difference, perhaps 20. So I might find
the lower tilt more to my liking. I think that if I raised my chair to match that it work better for me.
Stuff to experiment with.
Ok. chain up a notch. Does this really feel any better though? I can't really
tell that much of a difference except it seems to be crunching my shoulders
a bit. It sort of makes sense to me that some different muscles would be 
exercised in this rather different than flat hand position. 
I am certainly much more used to the relatively flat position than to
that raised one 
I will type more and see if I notice any difference that makes the tenting
really worth it to me.  So far I  don't really see it very much.
Having the chair up a bit is nicer ever without any tenting.  My arms 
are straighter. I could almost do with having more possible sreparation between 
the two halves.

Day 2 of messing about with tenting.  I think averall it is in the right 
direction modulo getting used to different keys being easier or harder
to reach and reprogramming some key-sequence muscle emmory. I still have a few more
typos but I notice that I much more seldom have an accidental control
key use type of error.

Sometimes my wrists hurt when using tented. May be how I am resting rellative
to the edge of my desk and height of my chair.  Which brings up one of the problems
of tented keyboard - I have to raise my chair up so much to have straight
forearm that my feet are not solidly on the floor. 
It feels sort of relaxing to go back to flat now and again.  Well, when 
I go back to flat my wrists hurt a lot faster.  or did I already hurt
them and just felt it more after?  
Sometimes it feels like my arms are slightly different lengths as what
feels fine for one arm doesn't necessarily work for the other. 


"""