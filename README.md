# NaughtyBoy

NaughtyBoy (nB) was created to make it easy to generate system or network
traffic for testing purposes.  This is super alpha... probably don't use it.

[<img src="http://i.imgur.com/ztmjt9o.gif">](https://www.youtube.com/watch?v=qCUUw2PRxh0#t=12)

## Configuration

nB takes a YAML configuration file that looks like:

```yaml
---
# seconds to sleep in-between iterations (to check on threads/processes)
sleep: 1

# commands to run before naughtyboy is started (i.e. for docker)
prep:
    - 'apt-get install curl'

# commands to run (forever)
commands:
    - 'curl http://vhost1.example.com'
    - 'curl http://vhost2.example.com ; sleep 5'
```

## Run With Python

```
$ pip install -r requirements.txt

$ python setup.py develop

$ python naughtyboy.py run commands.yml
Thread #0: curl -s http://vhost1.example.com/
Thread #1: curl -s http://vhost2.example.com/ ; sleep 5
Thread #0: curl -s http://vhost1.example.com/
Thread #0: curl -s http://vhost1.example.com/
Thread #0: curl -s http://vhost1.example.com/
Thread #0: curl -s http://vhost1.example.com/
Thread #0: curl -s http://vhost1.example.com/
Thread #1: curl -s http://vhost2.example.com/ ; sleep 5
...
```

By default, nB runs commands via threads, but can use processes as well:

```
$ python naughtyboy.py run commands.yml -m process
Process #0: curl -s http://vhost1.example.com/
Process #1: curl -s http://vhost2.example.com/ ; sleep 5
Process #0: curl -s http://vhost1.example.com/
Process #0: curl -s http://vhost1.example.com/
Process #0: curl -s http://vhost1.example.com/
Process #0: curl -s http://vhost1.example.com/
Process #0: curl -s http://vhost1.example.com/
Process #1: curl -s http://vhost2.example.com/ ; sleep 5
...
```

## Run With Docker

```
$ docker run -it -v /path/to/commands.yml:/app/commands.yml derks/naughtyboy
```

Or build it:

```
$ docker build -t naughtyboy:dev .

$ docker run -it -v /path/to/commands.yml:/app/commands.yml naughtyboy:dev
```
