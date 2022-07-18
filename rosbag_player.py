import asyncio
import pickle
from lemon import entrypoint, publish
import click
from collections.abc import Iterable
import genpy
import rosbag
import pickle
import yaml


def resolve_tmp_types(msg):
    if hasattr(msg, '_spec'):
        data = {}
        for attr in msg._spec.names:
            value = getattr(msg, attr)
            data[attr] = resolve_tmp_types(value)
        return data
    if isinstance(msg, Iterable):
        return [resolve_tmp_types(v) for v in msg]
    if isinstance(msg, genpy.Time):
        return {'sec': msg.secs, 'nsec': msg.nsecs}
    return msg


@click.command()
@click.argument('bag')
@click.argument('output')
@click.option('-m', '--mapping', default=None)
def convert(bag, output, mapping):
    """Convert a ROS BAG for fast processing. Use -m to point to a mapping file
    in .yml format mapping input to output topics. Example:

    bag_topic: my_topic
    other_bag_topic: my_other_topic
    ...
    """
    bag = rosbag.Bag(bag)
    data = []

    if mapping:
        with open(mapping, 'r') as file:
            mapping = yaml.safe_load(file)
            kwargs = {'topics': mapping.keys()}
    else:
        kwargs = {}

    for topic, msg, _ in bag.read_messages(**kwargs):
        data.append((
            topic if not mapping else mapping[topic], resolve_tmp_types(msg)))

    with open(output, 'wb') as f:
        pickle.dump(data, f)


@click.option('-f', '--file')
@entrypoint
async def start(file):
    with open(file, 'rb') as f:
        data = pickle.load(f)
    while True:
        for topic, msg in data:
            await publish(topic, msg)
            await asyncio.sleep(1e-2)
