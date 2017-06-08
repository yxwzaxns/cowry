import redis, time

r = redis.Redis(host='redis', port=6379, db=0)

while r.ping() != True:
    time.sleep(1)
