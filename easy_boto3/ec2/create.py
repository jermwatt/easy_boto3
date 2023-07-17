from easy_boto3.setup_session import setup
session_auth = setup()


@session_auth
def create_instance(KeyName: str,
                    InstanceName='example_worker',
                    InstanceType='t2.micro',
                    ImageId='ami-03f65b8614a860c29',
                    BlockDeviceMappings=None,
                    Groups=None,
                    UserData: str = None,
                    session=None) -> object:

    # create ec2 controller from session
    ec2_controller = session.resource('ec2')

    # translate startup_script if None
    if UserData is None:
        UserData = '#!/bin/bash'

    # create a new EC2 instance
    instances = ec2_controller.create_instances(
        ImageId=ImageId,
        NetworkInterfaces=[{
            'DeviceIndex': 0,
            'Groups': Groups,
            'AssociatePublicIpAddress': True}],
        UserData=UserData,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[{'ResourceType': 'instance',
                            'Tags': [{'Key': 'Name',
                                      'Value': InstanceName}]}],
        InstanceType=InstanceType,
        KeyName=KeyName,
        Monitoring={'Enabled': True},
        BlockDeviceMappings=BlockDeviceMappings,
        MetadataOptions={
            'HttpTokens': 'required',
            'HttpEndpoint': 'enabled'
        }
     )

    # Wait for the instance to be running
    instances[0].wait_until_running()

    # Print the instance ID
    print("Instance created:", instances[0].id)

    return instances[0]
