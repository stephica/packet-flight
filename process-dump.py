import re, fileinput


# hour, minute, sec, microsec, from, to, size. Note that these times are deltas
# so we'll only look at secs and usecs
reg = re.compile(r'^(\d\d):(\d\d):(\d\d)\.(\d+) IP (\S+) > (\S+): tcp (\d+)')

time = 0

machines = {}

spots = ((120, 240),(400,240))
spos = 0

for line in fileinput.input():
    m = reg.match(line)
    if m:
        hour, minu, sec, usec, src, dest, size = m.groups()

        start = time + (int(sec) * 1000000) + int(usec)

        ## add "latency" to any data packet.
        if int(size) > 0:
            start += 50000

        time = start

        if not machines.has_key(src):
            machines[src] = {'xy':spots[spos], 'packets':[]}
            spos += 1

        machines[src]['packets'].append((dest, start, int(size)))
    else:
        print "BLARGH", line

#print machines

for name, data in machines.iteritems():
    print '  nodes.put("%s", new NetworkNode("client", %d, %d));' % (name, data['xy'][0], data['xy'][1])


print '  NetworkNode node;'
for name, data in machines.iteritems():
    print '  node = (NetworkNode)nodes.get("%s");' % name
    for dest, start, size in data['packets']:
        print '  sprites.add(node.addPacket((NetworkNode)nodes.get("%s"), %d, %d));' % (dest, start, size)