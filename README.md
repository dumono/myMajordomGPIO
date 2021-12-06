# myMajordomGPIO
проект хаба умного дома на базе GPIO пинов мини-компьютеров

Для работы понадобится мини-ПК с GPIO и установленным на него дистрибутивом Debian(или производным)

Установка рекомендуется через ansible:
в папке install необходимо заполнить inventory.inv
где в качестве "you hub ip" указать ip-адрес Вашего мини-ПК

ansible-playbook -u "username" -k -i inventory.inv setup.yml

или ansible-playbook -u "username" -k -i "IP адрес" setup.yml

Имя пользователя и пароль по-умолчанию: admin / admin