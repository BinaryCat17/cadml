FROM nvcr.io/nvidia/physicsnemo/physicsnemo:25.11

# Устанавливаем SSH сервер
RUN apt-get update && apt-get install -y openssh-server && \
    mkdir -p /var/run/sshd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \  # отключаем пароль, только ключи
    rm -rf /var/lib/apt/lists/*

# Создаём директорию для ключей root
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh

WORKDIR /workspace

# Запускаем SSH и держим контейнер живым
CMD ["/usr/sbin/sshd", "-D"]
