# Getting-Started-Terraform

Welcome to Terraform - Getting Started.  These exercise files are meant to accompany my course on [Pluralsight](http://www.pluralsight.com/courses/terraform-getting-started-5).  The course was developed using version 1.12.2 of Terraform. Since the GA of version 1.0, HashiCorp has committed to no breaking changes until version 2.0. All the exercises in this course should be valid as long as you are using Terraform in the 1.X version family. The providers in this course have no such guarantee, so I have pinned the version where applicable.

If you're looking for the exercise files for older versions of the course, there are two branches to check out:

* [v4](https://github.com/ned1313/Getting-Started-Terraform/tree/v4) - Corresponding to the [course published in June 2023](http://www.pluralsight.com/courses/terraform-getting-started-2023)
* [v3](https://github.com/ned1313/Getting-Started-Terraform/tree/v3) - Corresponding to the [course published on Novemeber 2, 2021](https://app.pluralsight.com/library/courses/terraform-getting-started-2021/table-of-contents).
* [pre-1.0](https://github.com/ned1313/Getting-Started-Terraform/tree/pre-1.0) - Corresponding to the [course published on October 1, 2019](https://app.pluralsight.com/library/courses/getting-started-terraform/table-of-contents).

I don't recommend taking the older courses, as they are out of date and do not cover the latest features of Terraform.  I have left the branches available since you may be assigned an older course by your employer.

## Using the files

In the course, you are given a Terraform configuration for a basic web application from someone else on the Globomantics team. We are going to make a copy of this configuration and modify it over the length of the course. The `base_web_app` directory has the basic web app configuration, which we will copy over to a new directory called `globo_web_app`, and start making alterations.

As we progress through the course, you will be challenged to make updates to the files in `globo_web_app` to meet the evolving needs and requirements of the web application infrastructure. The completed solution for each module is in the `mX_solution` directories. I recommend trying to first write the solution yourself, and then checking your answer against what you see in the solution file.

In previous versions of the course I started with hardcoded credentials in the provider block and then used input variables to remove them. Putting your credentials in code is a **terrible** idea, and while my goal was to illustrate how Terraform gets those credentials and how input variables and shell environment variables are helpful, I've decided the practice is too egregious to include even as an anti-pattern. As such, the course assumes you have stored AWS credentials in environment variables or through the AWS CLI as a profile. If you're unfamiliar with how to accomplish this, please check out the documentation [here for environment variables](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#environment-variables) and [here for configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-authentication-user.html).

The suggested commands for each module are in the `commands` directory. You can run these commands to get through the exercises, but I also encourage you to experiment and try things out for yourself.

## Providers

This course uses the AWS provider. I have pinned the version to stay on major version 5. When writing this course, version 6 was still very early in its release cycle and had already encountered some major issues. I chose to stay on version 5 to ensure the stability of the course. You can try out version 6 if you'd like!

## AWS Environment

You will need access to an AWS environment with permissions to create resources in EC2 and S3. I recommend creating a dedicated account just for this course. The exercises have been tested with AWS region `us-east-1`. The input variable `aws_region` has `us-east-1` set as the default, but you can supply a different region if you prefer. Generally, the exercises should work in any region that has the Amazon Linux 2 AMI and `t3.micro` size instances (although you can adjust that as well).

You will need to generate an AWS access key to run through the exercises. You can do this through the IAM console in a browser (*hint*: it's under security credentials for your user) by following the [official AWS docs](https://aws.amazon.com/premiumsupport/knowledge-center/create-access-key/). I'd recommend assigning the `AdministratorAccess` policy to your user to give you permissions to do everything in the account. Also, enable 2FA for the user account!

## Line Endings

An issue I have discovered from time to time is that Terraform doesn't much like the Windows style of ending a line with both a Carriage Return (CR) and a Line Feed (LF), commonly referred to as CRLF.  If you are experiencing strange parsing issues, change the line ending to be Line Feed (LF) only.  In VS Code this can be down by clicking on the CRLF in the lower right corner and changing it to LF. This primarily affects template files or scripts being sent to a Linux machine for processing.

## MONEY!!!

A gentle reminder about cost.  The course will have you creating resources in AWS.  AWS recently replaced their original free tier offering with a new [Free Plan account](https://aws.amazon.com/free/) that includes up to $200 in credits and some always free services. If you open a new account after July 2025, you should be able to use that account with this course and not incur any costs.

The new Free Plan does limit your consumption of services. To avoid hitting that limit, you should remove resources when not actively taking the course. When you complete an exercise in the course, you can easily tear down the deployed infrastructure using `terraform destroy`. Just run that command and approve the destruction to remove all resources from AWS. Before you start the next module, run `terraform apply` again and you should be right where you started. Isn't infrastructure automation amazing?!

## Certification

HashiCorp offers the Terraform Certified Associate certification. You might be wondering if this course fully prepares you for the cert.  **It does not.**  Taking this course along with the rest of the Terraform learning path on Pluralsight should cover all the objectives on the exam and give you the knowledge you need to pass.

I have coauthored a certification guide which you can find on [Leanpub](https://leanpub.com/terraform-certified/). This is an unofficial guide, but I believe in concert with the Pluralsight courses you will be in a good position to sit the exam. And in case you're wondering, yes it is fully updated for version 003 of the exam that was released in May 2023.

## Conclusion

I hope you enjoy taking this course as much as I did creating it.  I'd love to hear feedback and suggestions for revisions. Find me on LinkedIn (https://www.linkedin.com/in/ned-bellavance/) or add an issue to this repository.

Thanks and happy automating!

Ned
