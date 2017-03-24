FROM centos:centos7
MAINTAINER Hiroyuki Kojima <hiroyuki.kojima@fxss.co.jp>

RUN localedef -f UTF-8 -i ja_JP ja_JP.utf8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

RUN yum -y update
RUN yum -y install gcc gcc-c++ make git openssl-devel tar zlib-devel readline-devel which wget bzip2 patch libffi-devel gdbm-devel libyaml-devel

# rbenvインストール
RUN git clone https://github.com/sstephenson/rbenv.git /root/.rbenv
RUN git clone https://github.com/sstephenson/ruby-build.git /root/.rbenv/plugins/ruby-build
RUN ./root/.rbenv/plugins/ruby-build/install.sh
ENV PATH /root/.rbenv/bin:$PATH
RUN echo 'export PATH=/root/.rbenv/bin:$PATH' >> /root/.bashrc
RUN echo 'eval "$(rbenv init -)"' >> /root/.bashrc

# rubyインストール
ENV CONFIGURE_OPTS --disable-install-doc
RUN rbenv install -v 2.4.0; rbenv rehash; rbenv global 2.4.0
ENV PATH /root/.rbenv/versions/2.4.0/bin:$PATH
RUN echo 'export PATH=/root/.rbenv/versions/2.4.0/bin:$PATH' >> /root/.bashrc

# RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -C '' -N ''
# RUN ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key -C '' -N ''

# 証明書取得(gem用)
# 「gem which rubygems」コマンドで取得したrubygemの格納場所から証明書の格納場所を確定
# 参考: http://qiita.com/c0rtashma/items/84743c4741fef65e3b8f
RUN mkdir -p /root/.rbenv/versions/2.4.0/lib/ruby/2.4.0/rubygems/ssl_certs
RUN cd /root/.rbenv/versions/2.4.0/lib/ruby/2.4.0/rubygems/ssl_certs; \
    wget https://raw.githubusercontent.com/rubygems/rubygems/master/lib/rubygems/ssl_certs/index.rubygems.org/GlobalSignRootCA.pem

# wikipediaのコーパスを作成するパッケージ(wp2txt)インストール
RUN gem install bundle
RUN mkdir /root/ruby_bundle
RUN cd /root/ruby_bundle; bundle init; echo 'gem "wp2txt"' >> Gemfile; bundle install

CMD ["/bin/bash"]
