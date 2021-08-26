from multiprocessing import Process, Pipe
from datetime import datetime


def local_time(ts):
    return f' (LAMPORT_TIMESTAMP = {ts})'


def calc_recv_timestamp(recv_time_stamp, ts):
    return max(recv_time_stamp, ts) + 1


def event(pid, ts):
    ts += 1
    print(f'Event in {pid} !' + local_time(ts))
    return ts


def send_message(pipe, pid, receiver, ts):
    ts += 1
    pipe.send(('Msg', ts))
    print(f'Message sent from {str(pid)} to {receiver}' + local_time(ts))
    return ts


def recv_message(pipe, pid, sender, ts):
    message, timestamp = pipe.recv()
    ts = calc_recv_timestamp(timestamp, ts)
    print(f'Message received at {str(pid)} from {sender}' + local_time(ts))
    return ts


def process_one(pipe12, pipe13):
    pid = 'P1'
    ts, p1 = 0, []
    p1.append(ts)
    ts = event(pid, ts)
    p1.append(ts)
    ts = send_message(pipe12, pid, 'P2', ts)    # Process 1 sending message to Process 2
    p1.append(ts)
    ts = event(pid, ts)
    p1.append(ts)
    ts = recv_message(pipe12, pid, 'P2', ts)    # Process 1 receiving message from Process 2
    p1.append(ts)
    ts = send_message(pipe13, pid, 'P3', ts)    # Process 1 sending message to Process 3
    p1.append(ts)
    print(f'P1 Timestamps: {p1}\n')


def process_two(pipe21, pipe23):
    pid = 'P2'
    ts, p2 = 0, []
    p2.append(ts)
    ts = recv_message(pipe23, pid, 'P3', ts)    # process 2 receiving message from process 3
    p2.append(ts)
    ts = recv_message(pipe21, pid, 'P1', ts)    # process 2 receiving message from process 1
    p2.append(ts)
    ts = send_message(pipe21, pid, 'P1', ts)    # process 2 sending message to process 1
    p2.append(ts)
    print(f'P2 Timestamps: {p2}\n')


def process_three(pipe32, pipe31):
    pid = 'P3'
    ts, p3 = 0, []
    p3.append(ts)
    ts = send_message(pipe32, pid, 'P2', ts)    # process 3 sending message to process 2
    p3.append(ts)
    ts = event(pid, ts)
    p3.append(ts)
    ts = recv_message(pipe31, pid, 'P1', ts)    # process 3 receiving message from process 1
    p3.append(ts)
    print(f'P3 Timestamps: {p3}\n')


if __name__ == '__main__':
    one_two, two_one = Pipe()
    two_three, three_two = Pipe()
    three_one, one_three = Pipe()

    process1 = Process(target=process_one, args=(one_two, one_three))
    process2 = Process(target=process_two, args=(two_one, two_three))
    process3 = Process(target=process_three, args=(three_two, three_one))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
