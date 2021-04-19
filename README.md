# ec2-state-ctrl
Web page to control state of EC2 instances (check state, stop and start).

## Usage:

docker build -t capic-control .
docker run -d -p 80:80 --name=capic-control -e AWS_ACCESS_KEY_ID=<your_key> -e AWS_SECRET_ACCESS_KEY=<your_secret> capic-control
