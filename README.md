# Welcome to my first CDK project[s]

Here you will learn to use CDK to deploy different AWS resources. All the `sample code` are tagged with intuitive tag-names.

1. ## 🧰 Prerequisites

   - 🛠 AWS CLI Installed & Configured - [Get help here](https://youtu.be/TPyyfmQte0U)
   - 🛠 AWS CDK Installed & Configured - [Get help here](https://www.youtube.com/watch?v=MKwxpszw0Rc)
   - 🛠 Python Packages, _Change the below commands to suit your operating system, the following are written for \_Amazon Linux 2_
     - Python3 - `yum install -y python3`
     - Python Pip - `yum install -y python-pip`
     - Virtualenv - `pip3 install virtualenv`

1. ## ⚙️ Setting up the environment

   For example, If you are looking to learn how to deploy an EC2 instance with the latest AMI in any region, This branch is tagged as `ec2_with_latest_ami_in_any_region`.

   ```bash
   git clone --branch ec2_with_latest_ami_in_any_region https://github.com/miztiik/my-first-cdk-project.git
   cd my-first-cdk-project
   ```

1. ## 🚀 Deployment using AWS CDK

   ```bash
   # If you DONT have cdk installed
   npm install -g aws-cdk
   # If this is first time you are using cdk then, run cdk bootstrap
   # cdk bootstrap


   # Make sure you in root directory
   python3 -m venv .env
   source .env/bin/activate
   # Install any dependencies
   pip install -r requirements.txt

   # Synthesize the template and deploy it
   cdk synth
   cdk deploy
   ```

1. ## 🧹 CleanUp

   If you want to destroy all the resources created by the stack, Execute the below command to delete the stack, or _you can delete the stack from console as well_

   ```bash
   cdk destroy *
   ```

   This is not an exhaustive list, please carry out other necessary steps as maybe applicable to your needs.

### 💡 Help/Suggestions or 🐛 Bugs

Thank you for your interest in contributing to our project. Whether it is a bug report, new feature, correction, or additional documentation or solutions, we greatly value feedback and contributions from our community. [Start here][200]

### 👋 Buy me a coffee

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Q5Q41QDGK) Buy me a [coffee ☕][900].

### 🏷️ Metadata

**Level**: 200

![miztiik-success-green](https://img.shields.io/badge/miztiik-cdk-success-green)

[100]: https://www.udemy.com/course/aws-cloud-security/?referralCode=B7F1B6C78B45ADAF77A9
[101]: https://www.udemy.com/course/aws-cloud-security-proactive-way/?referralCode=71DC542AD4481309A441
[102]: https://www.udemy.com/course/aws-cloud-development-kit-from-beginner-to-professional/?referralCode=E15D7FB64E417C547579
[103]: https://www.udemy.com/course/aws-cloudformation-basics?referralCode=93AD3B1530BC871093D6
[200]: https://github.com/miztiik/my-first-cdk-project/issues
[899]: https://www.udemy.com/user/n-kumar/
[900]: https://ko-fi.com/miztiik
[901]: https://ko-fi.com/Q5Q41QDGK
