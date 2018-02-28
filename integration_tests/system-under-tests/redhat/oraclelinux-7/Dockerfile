FROM oraclelinux:7

RUN yum install -y openssh-server
RUN mkdir /var/run/sshd
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N ''
RUN echo 'root:phial' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

ENV LANG en_US.UTF-8

COPY ./setup.sh /puppeter-setup.sh
RUN chmod +x /puppeter-setup.sh
ENV MODE dependencies
RUN /puppeter-setup.sh

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
