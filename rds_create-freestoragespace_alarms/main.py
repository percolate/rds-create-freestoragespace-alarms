#!/usr/bin/env python
"""rds_create_freestoragespace_alarms

Script used to create a below 20 pct. Low-FreeStorageSpace alarm
in AWS CloudWatch for all RDS instances

Usage:
    rds_create_freestoragespace_alarms [options]
    rds_create_freestoragespace_alarms [-h | --help]

Options:
     --debug   Don't send data to AWS

"""
import boto.ec2
import boto.rds2
from docopt import docopt
from boto.ec2.cloudwatch import MetricAlarm

DEBUG = False


def get_rds_instances():
    """
    Retreives the list of all RDS instances

    Returns:
        (list) List of valid state RDS instances
    """
    rds = boto.connect_rds2()
    response = rds.describe_db_instances()
    rds_instances = (response[u'DescribeDBInstancesResponse']
                             [u'DescribeDBInstancesResult']
                             [u'DBInstances'])

    return rds_instances


def get_existing_freestoragespace_alarm_names(aws_cw_connect):
    """
    Creates a Low-FreeStorageSpace alarm for all RDS instances

    Args:
        aws_cw_connect (CloudWatchConnection)

    Returns:
        (set) Existing Low-FreeStorageSpace alarm names
    """
    assert isinstance(aws_cw_connect,
                      boto.ec2.cloudwatch.CloudWatchConnection)

    existing_alarms = aws_cw_connect.describe_alarms()
    existing_alarm_names = set()

    for existing_alarm in existing_alarms:
        existing_alarm_names.add(existing_alarm.name)

    return existing_alarm_names


def get_freestoragespace_alarms_to_create(rds_instances,
                                          aws_cw_connect):
    """
    Creates a Low-FreeStorageSpace alarm for all RDS instances

    Args:
        rds_instances (list) ist of all RDS instances
        aws_cw_connect (CloudWatchConnection)

    Returns:
        (set) All Low-FreeStorageSpace alarms that will be created
    """
    assert isinstance(rds_instances, list)
    assert isinstance(aws_cw_connect,
                      boto.ec2.cloudwatch.CloudWatchConnection)

    alarms_to_create = set()
    existing_alarms = get_existing_freestoragespace_alarm_names(aws_cw_connect)

    for instance in rds_instances:

        # initiate a MetricAlarm object for
        # each RDS instance
        # for the threshold we calculate the 20 percent
        # from the instances' AllocatedStorage value and
        # convert them to bytes
        freestorage_alarm = MetricAlarm(
            name=u'RDS-{}-Low-Free-Storage-Space'.format(
                instance[u'DBInstanceIdentifier']),
            namespace=u'AWS/RDS',
            metric=u'FreeStorageSpace', statistic='Average',
            comparison=u'<',
            threshold=(0.20*instance[u'AllocatedStorage'])*1000000000,
            period=60, evaluation_periods=5,
            alarm_actions=[u'arn:aws:sns:us-west-1:667005031541:ops'],
            dimensions={u'DBInstanceIdentifier':
                        instance[u'DBInstanceIdentifier']})

        if freestorage_alarm.name not in existing_alarms:
            alarms_to_create.add(freestorage_alarm)

    return alarms_to_create


def main():
    args = docopt(__doc__)

    global DEBUG

    if args['--debug']:
        DEBUG = True

    rds_instances = get_rds_instances()
    aws_cw_connect = boto.connect_cloudwatch()
    alarms_to_create = get_freestoragespace_alarms_to_create(rds_instances,
                                                             aws_cw_connect)

    if alarms_to_create:
        if DEBUG:
            for alarm in alarms_to_create:
                print 'DEBUG:', alarm
        else:
            print 'New RDS Low-FreeStorageSpace Alarms created:'
            for alarm in alarms_to_create:
                print alarm
                aws_cw_connect.create_alarm(alarm)


if __name__ == '__main__':

    main()
