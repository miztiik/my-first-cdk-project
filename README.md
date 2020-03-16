
# Welcome to my first CDK project[s]

Here you will learn to use CDK to deploy different AWS resources. All the `sample code` are tagged with intuitive tag-names.

1. ## 🧰 Prerequisites

    - 🛠 AWS CLI Installed & Configured - [Get help here](https://youtu.be/TPyyfmQte0U)
    - 🛠 AWS CDK Installed & Configured - [Get help here](https://www.youtube.com/watch?v=MKwxpszw0Rc)

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

## 👋 Buy me a coffee

Buy me a coffee ☕ through [Paypal](https://paypal.me/valaxy), _or_ You can reach out to get more details through [here](https://youtube.com/c/valaxytechnologies/about).

### 💡 Help/Suggestions or 🐛 Bugs

- [Github Issues](https://github.com/miztiik/my-first-cdk-project/issues)

### ℹ️ Metadata

**Level**: 200
