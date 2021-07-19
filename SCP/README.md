# SCP

This folder contains an example SCP to prevent the User from interacting with Elastic Beanstalk directly and to protect the resources deployed by this solution from unauthorized changes.  
**Note: This SCP should only work as a starting point. It is very likely that further adjustments are needed to effectively implement this SCP in your environment.**

The idea of this SCP is, to use mainly naming conventions, like `SC-*` or `CF-*` matching names, to identify resources which are not allowed to be created/changed/deleted by everybody.  
The `SC-*` prefix is created by Service Catalog automatically. Keep in mind that IAM roles created by other Service Catalog products may have this prefix and thus would be allowed to change the resources deployed by the Elastic Beanstalk product.

To ensure, that IAM roles linked to resources deployed by the Elastic Beanstalk product can perform needed actions, a condition is used which exclude these IAM Roles from the deny statements.  
If additional IAM roles should be allowed to change the resources directly, the list needs to be adapted accordingly.

EC2 actions are denied based on tags instead of based on naming, since the EC2 instances are created by Elastic Beanstalk. Thus, there is no control over the naming of these resources. However, these resources can be tagged, why a tag-based authorization logic is used here.
