FROM centos:centos7
MAINTAINER Hiroyuki Kojima <hiroyuki.kojima@fxss.co.jp>

RUN localedef -f UTF-8 -i ja_JP ja_JP.utf8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

RUN yum install -y wget tar vi bzip2
RUN yum install -y gcc make gcc-c++
RUN yum install -y perl perl-devel
#RUN yum install -y nkf
RUN yum localinstall -y http://mirror.centos.org/centos/6/os/x86_64/Packages/nkf-2.0.8b-6.2.el6.x86_64.rpm

# Mecab
RUN wget -O mecab-0.996.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE"
RUN tar -xzf mecab-0.996.tar.gz
RUN cd mecab-0.996; ./configure --enable-utf8-only; make; make install; ldconfig

# Ipadic
RUN wget -O mecab-ipadic-2.7.0-20070801.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM"
RUN tar -xzf mecab-ipadic-2.7.0-20070801.tar.gz
RUN cd mecab-ipadic-2.7.0-20070801; ./configure --with-charset=utf8; make; make install
RUN echo "dicdir = /usr/local/lib/mecab/dic/ipadic" > /usr/local/etc/mecabrc

# Ipadic_model
RUN wget -O mecab-ipadic-2.7.0-20070801.model.bz2 "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7bnc5aFZSTE9qNnM"
RUN bzip2 -d mecab-ipadic-2.7.0-20070801.model.bz2
#RUN iconv -f EUCJP -t UTF-8 mecab-ipadic-2.7.0-20070801.model -o mecab-ipadic-2.7.0-20070801.model
RUN nkf --overwrite -Ew mecab-ipadic-2.7.0-20070801.model
RUN sed -i -e "s/euc-jp/utf-8/g" mecab-ipadic-2.7.0-20070801.model

# Mecab-perl
RUN wget -O mecab-perl-0.996.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7M1pQam5XQjBLcU0"
RUN tar -xzf mecab-perl-0.996.tar.gz
RUN cd mecab-perl-0.996 ;perl Makefile.PL; make ;make install;
RUN echo "/usr/local/lib" > /etc/ld.so.conf.d/mecab.conf
RUN ldconfig

# PerlのDB_Fileインストール
RUN wget http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/DB_File-1.840.tar.gz
RUN tar -xzf DB_File-1.840.tar.gz
RUN cd DB_File-1.840; \
    sed -i".org" -e "/^INCLUDE/a INCLUDE = /usr/local/BerkeleyDB.5.5/include" config.in; \
    sed -i -e "1,/^INCLUDE/s/^INCLUDE/#INCLUDE/" config.in; \
    sed -i -e "/^LIB/a LIB = /usr/local/BerkeleyDB.5.5/lib" config.in; \
    sed -i -e "1,/^LIB/s/^LIB/#LIB/" config.in; \
    perl Makefile.PL; make; make test; make install

# TermExtract
RUN wget http://gensen.dl.itc.u-tokyo.ac.jp/soft/TermExtract-4_10.tar.gz
RUN tar -xzf TermExtract-4_10.tar.gz
RUN nkf --overwrite -Ew /TermExtract-4_10/TermExtract/MeCab.pm
RUN cd TermExtract-4_10 ;perl Makefile.PL; make ;make install

# Add perl script
ADD termextract_mecab.pl /usr/local/bin/termextract_mecab.pl
RUN chmod 755 /usr/local/bin/termextract_mecab.pl

# Clean up
RUN rm -rf mecab-0.996.tar.gz*
RUN rm -rf mecab-ipadic-2.7.0-20070801.tar.gz*
RUN rm -rf mecab-perl-0.996.tar.gz*
RUN rm -rf TermExtract-4_10.tar.gz*
RUN rm -rf DB_File-1.840.tar.gz*
