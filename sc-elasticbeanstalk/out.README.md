|Parameter|Type|Default|Description|
----
|### VPCId | AWS::EC2::VPC::Id  | | The of the VPC that the elastic beanstalk application will be in. |
|### EC2SubnetIds | List<AWS::EC2::Subnet::Id>  | | The id of the one (or more) Subnets that the elastic beanstalk instances will be in. |
|### ELBSubnetIds | List<AWS::EC2::Subnet::Id>  | | The id of the one (or more) Subnets that the elastic beanstalk loadbalancer will be in. |
|### EC2SecurityGroupId | String  | | Provide security groups for the EC2 Instances - optional |
|### ELBSecurityGroupId | String  | | Provide security groups for the Loadbalancer - optional |
|### SolutionStackName | String | 64bit Amazon Linux 2 v3.2.1 running PHP 8.0 | Enter the name of the solution stack. A list of available Solution Stacks can be found here:https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/platforms-supported.html. |
|### ApplicationName | String  | | The name of the Elastic Beanstalk Application |
|### LoadBalancerType | String | application | Loadbalancer type |
|### ClusterMinInstances | Number | 1 | Minimum number of cluster instances for autoscaling |
|### ClusterMaxInstances | Number | 4 | Maximum number of cluster instances for autoscaling |
|### InstanceTypes | String  | Optional - A comma-separated list of instance types you want your environment to use. For example t2.micro,t3.micro |
|### ElasticBeanstalkRole | String  | Optional - IAM Role attached to the instance profiles of the Elastic Beanstalk instances. Default containing AWSElasticBeanstalkWebTier, AWSElasticBeanstalkMulticontainerDocker and AWSElasticBeanstalkWorkerTier AWS managed policies. |
|### CloudWatchLogsRetentionInDays | String | 400 | Optional - The number of days to keep CloudWatch Logs log events before they expire. Default is 7. |
|### RollingUpdateType | String | Health | Configuration Update - Time-based rolling updates apply a PauseTime between batches. Health-based rolling updates wait for new instances to pass health checks before moving on to the next batch. Immutable updates launch a full set of instances in a new Auto Scaling group. |
|### MaxBatchSize | String  | Optional - Configuration Update - The number of instances included in each batch of the rolling update. Default - One-third of the minimum size of the Auto Scaling group, rounded to the next highest integer. |
|### MinInstancesInService | String  | Optional - Configuration Update - The minimum number of instances that must be in service within the Auto Scaling group while other instances are terminated. Default - The minimum size of the Auto Scaling group or one less than the maximum size of the Auto Scaling group, whichever is lower. |
|### PreferredStartTime | String | Tue:09:00 | Managed Updates - Configure a maintenance window for managed actions in UTC |
|### SSLCertificateArn | String  | Optional - ARN of SSL Certificate uploaded to IAM - The provided certificate is used to terminate the SSL traffic on the LoadBalancer (ALB or CLB). If empty, LoadBalancer listens on Port 80 (HTTP). This value is ignored for Network Load Balancer type. |
|### CLBInstancePort | String | 80 | Optional - InstancePort used for Classical Load Balancer. If empty, the default value is used (443 for SSL Termination on Classic Load Blaancer). This field is ignored for other Load Balancer Types. |
|### GlobalAllowlistBucketPrefix | String | cf-ebextensions-validator-allowlist | Static - bucket name prefix for ebextensions validator allowlist bucket |
|### GlobalAllowlistFolderName | String | global | Static - global allowlist folder name for ebextensions validator |
