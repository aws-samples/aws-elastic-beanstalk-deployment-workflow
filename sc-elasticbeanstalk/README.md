# sc-elasticbeanstalk

This folder contains the AWS Elastic Beanstalk resources and StateMachine to deploy and update application code.  

## application_deployment

This folder contains the CloudFormation template `application_deployment.yaml` and Python code for Lambda functions. The template contains the AWS Step Functions state machine which is used to deploy and update the Application code. More information on the state machine can be found in the [application_deployment](application_deployment) folder itself.  
You also find unit-tests in this folder for the *ebextensions_validator* Python code.

## ec2KeyPairDummy

This lambda function creates an EC2 key pair for the Elastic Beanstalk environment. It is set during the initial creation of the environment, so that it cannot be overwritten by .ebextensions later on (see https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options.html#configuration-options-precedence). The private key is not saved anywhere, so that it is not possible to use this EC2 key pair to log into the instances via SSH.

## sc-elasticbeanstalk-ra.yaml

This CloudFormation template contains the Elastic Beanstalk Application and Environment. The template itself is non-functional, since the list of available `SolutionStackNames` is not present. You need to apply `update_solution_stack_list.sh` to this template first:

```
sh update_solution_stack_list.sh sc-elasticbeanstalk-ra.yaml > sc-elasticbeanstalk-ra_DEPLOYABLE.yaml
```
*Note*: This step is not needed if you use the instructions in the "Install" section [here](/README.md) or one of the CICD options in [CICD](../CICD).

This template also contains `application_deployment/application_deployment.yaml` as a nested stack.  
The `ApplicationDeploymentRole` defined in [application_deployment.yaml](application_deployment/application_deployment.yaml) is the IAM role which effectively will update the Beanstalk Environment. It will also deploy AWS Resources if defined in the `.ebextensions` files. Make sure that this IAM Role has all the permissions needed to deploy the Resources you want to be deployed in an Elastic Beanstalk Environment

Following is the list of parameters defined in the Service Catalog product. These can be set by the User.  
All parameters which are not marked as **optional** are required. Most of them are already prepopulated with valid values.  
**The only parameters which need to be set are *VPCId*, *EC2SubnetIDs* and *ELBSubnetIds*.**. Make sure, that the EC2 Subnets have connectivity to the AWS API (e.g. via a NAT gateway) and that the ELB Subnets are reachable from where you want to access the application running in Elastic Beanstalk (e.g. public internet). Find more information on the VPC configurations in the [AWS documentation](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/vpc.html).  
The two **static** parameters *GlobalAllowlistBucketPrefix* and *GlobalAllowlistFolderName* are fixed and depend on the parameters set for the [allowlist-bucket](../allowlist-bucket) template.  
|Parameter|Type|Default|Description|
|-|-|-|-|
| VPCId | AWS::EC2::VPC::Id  | | The of the VPC that the elastic beanstalk application will be in. |
| EC2SubnetIds | List<AWS::EC2::Subnet::Id>  | | The id of the one (or more) Subnets that the elastic beanstalk instances will be in. |
| ELBSubnetIds | List<AWS::EC2::Subnet::Id>  | | The id of the one (or more) Subnets that the elastic beanstalk loadbalancer will be in. |
| EC2SecurityGroupId | String  | | **Optional** - Provide security groups for the EC2 Instances |
| ELBSecurityGroupId | String  | | **Optional** - Provide security groups for the Loadbalancer |
| SolutionStackName | String | *Default value generated via updated_solution_stack_list.sh* | Enter the name of the solution stack. A list of available Solution Stacks can be found here:https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/platforms-supported.html. |
| ApplicationName | String  | | The name of the Elastic Beanstalk Application |
| LoadBalancerType | String | application | Loadbalancer type |
| ClusterMinInstances | Number | 1 | Minimum number of cluster instances for autoscaling |
| ClusterMaxInstances | Number | 4 | Maximum number of cluster instances for autoscaling |
| InstanceTypes | String | | **Optional** - A comma-separated list of instance types you want your environment to use. For example t2.micro,t3.micro |
| ElasticBeanstalkRole | String | | **Optional** - IAM Role attached to the instance profiles of the Elastic Beanstalk instances. Default containing AWSElasticBeanstalkWebTier, AWSElasticBeanstalkMulticontainerDocker and AWSElasticBeanstalkWorkerTier AWS managed policies. |
| CloudWatchLogsRetentionInDays | String | 400 | **Optional** - The number of days to keep CloudWatch Logs log events before they expire. Default is 7. |
| RollingUpdateType | String | Health | Configuration Update - Time-based rolling updates apply a PauseTime between batches. Health-based rolling updates wait for new instances to pass health checks before moving on to the next batch. Immutable updates launch a full set of instances in a new Auto Scaling group. |
| MaxBatchSize | String | | **Optional** - Configuration Update - The number of instances included in each batch of the rolling update. Default - One-third of the minimum size of the Auto Scaling group, rounded to the next highest integer. |
| MinInstancesInService | String | | **Optional** - Configuration Update - The minimum number of instances that must be in service within the Auto Scaling group while other instances are terminated. Default - The minimum size of the Auto Scaling group or one less than the maximum size of the Auto Scaling group, whichever is lower. |
| PreferredStartTime | String | Tue:09:00 | Managed Updates - Configure a maintenance window for managed actions in UTC |
| SSLCertificateArn | String | | **Optional** - ARN of SSL Certificate uploaded to IAM - The provided certificate is used to terminate the SSL traffic on the LoadBalancer (ALB or CLB). If empty, LoadBalancer listens on Port 80 (HTTP). This value is ignored for Network Load Balancer type. |
| CLBInstancePort | String | 80 | **Optional** - InstancePort used for Classical Load Balancer. If empty, the default value is used (443 for SSL Termination on Classic Load Blaancer). This field is ignored for other Load Balancer Types. |
| GlobalAllowlistBucketPrefix | String | cf-ebextensions-validator-allowlist | **Static** - bucket name prefix for ebextensions validator allowlist bucket |
| GlobalAllowlistFolderName | String | global | **Static** - global allowlist folder name for ebextensions validator |

## update_solution_stack_list.sh

This two-line bash script fetches the current list of supported platforms, it removes the Docker related platforms and transforms the output into a yaml compatible list object. This script is used to replace the placeholder `REPLACE_ME_SOLUTIONSTACKNAME` in the `sc-elasticbeanstalk-ra.yaml` with the current list of supported and compliant platforms. It also sets a valid default value for this parameter by replacing the placeholder `REPLACE_ME_DEFAULT_SOLUTIONSTACKNAME`.  
In case further requirements to the solution stacks come up, another way of handling the creation of the allowed list of `SolutionStackNames` may need to be found.

## Usage

For more information how to use the solution, see the "User" section in [docs](../docs)
