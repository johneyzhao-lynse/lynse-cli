FROM alpine:3.19

RUN apk add --update --no-cache curl ca-certificates bash bash-completion zsh ncurses util-linux

ADD client.sh /usr/bin/client.sh
ADD _client.sh /usr/local/share/zsh/site-functions/_client.sh
ADD client.sh.bash-completion /etc/bash-completion.d/client.sh
RUN chmod 755 /usr/bin/client.sh

# 创建非 root 用户
RUN adduser -D -s /bin/zsh appuser

# Install oh-my-zsh for appuser
USER appuser
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" || true

# Enable bash completion
USER root
RUN echo '\n\
. /etc/bash_completion\n\
source /etc/bash-completion.d/client.sh\n\
' >> /home/appuser/.bashrc

# Setup prompt
RUN echo 'export PS1="[OpenAPI definition] \$ "' >> /home/appuser/.bashrc
RUN echo 'export PROMPT="[OpenAPI definition] \$ "' >> /home/appuser/.zshrc

# Setup a welcome message
RUN echo -e 'echo "\
\n\
This Docker provides preconfigured environment for running the command\n\
line REST client for $(tput setaf 6)OpenAPI definition$(tput sgr0).\n\
\n\
$(tput setaf 7)Basic usage:$(tput sgr0)\n\
\n\
$(tput setaf 3)Print the list of operations$(tput sgr0)\n\
$ client.sh -h\n\
\n\
$(tput setaf 3)Print the service description$(tput sgr0)\n\
$ client.sh --about\n\
\n\
$(tput setaf 3)Print help for specific operation$(tput sgr0)\n\
$ client.sh <operationId> -h\n\
\n\
"' | tee -a /home/appuser/.bashrc /home/appuser/.zshrc

# 设置工作目录权限
RUN chown -R appuser:appuser /home/appuser

USER appuser
WORKDIR /home/appuser

ENTRYPOINT ["/bin/zsh"]
