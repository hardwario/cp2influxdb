'COOPER to InfluxDB'

import click
import datetime
import influxdb
import json
import logging.config
import sys
import yaml
import zmq
from .config import load_config

__version__ = '@@VERSION@@'

MEASUREMENTS = [
    'altitude',
    'co2-conc',
    'humidity',
    'illuminance',
    'motion-count',
    'orientation',
    'press-count',
    'pressure',
    'rssi',
    'sequence',
    'sound-level',
    'temperature',
    'voc-conc',
    'voltage',
]


@click.command()
@click.option('--config', '-c', 'config_file', type=click.File('r'),
              required=True, help='Configuration file.')
@click.option('--test', is_flag=True, help='Test configuration file.')
@click.version_option(version=__version__)
def main(config_file, test=False):
    try:
        config = load_config(config_file)
        config_file.close()
        if test:
            click.echo("The configuration file seems ok")
            return
        logging.config.dictConfig(config['log'])
        logging.info('Process started')
        server(config)
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        pass


def server(config):
    context = zmq.Context()
    sock = context.socket(zmq.SUB)
    sock.setsockopt_string(zmq.SUBSCRIBE, '')
    sock.connect('tcp://%s:%d' %
        (config['zmq']['host'], config['zmq']['port']))
    try:
        db = influxdb.InfluxDBClient(
            host=config['influxdb']['host'],
            port=config['influxdb']['port'],
            username=config['influxdb']['username'],
            password=config['influxdb']['password'],
            database=config['influxdb']['database'])
        db.create_database(config['influxdb']['database'])
    except Exception as e:
        logging.error('Failed to create InfluxDB client', exc_info=True)
        sys.exit(1)
    while True:
        try:
            message = sock.recv_json()
            time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            points = []
            for k, v in message.items():
                if k in MEASUREMENTS and v is not None:
                    points.append({
                        'measurement': k,
                        'time': time,
                        'tags': {
                            'id': message['id'],
                            'gw': message['gw'],
                        },
                        'fields': {
                            'value': v
                        }
                    })
            db.write_points(points)
        except zmq.error.Again as e:
            logging.error('ZeroMQ error: %s' % e)
        except Exception:
            logging.error('Unhandled exception', exc_info=True)
