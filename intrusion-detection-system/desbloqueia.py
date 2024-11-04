import os
import re
import subprocess

def listar_regras_bloqueio():
    result = subprocess.run(["sudo", "iptables", "-L", "INPUT", "-n", "--line-numbers"],
                            capture_output=True, text=True)
    regras = result.stdout.splitlines()
    bloqueios = []

    for regra in regras:
        if "DROP" in regra:
            partes = regra.split()
            linha = partes[0]
            ip_bloqueado = partes[-1]
            bloqueios.append((linha, ip_bloqueado))

    return bloqueios

def desbloquear_ips():
    bloqueios = listar_regras_bloqueio()

    for linha, ip in reversed(bloqueios):
        print(f"Desbloqueando IP: {ip}")
        os.system(f"sudo iptables -D INPUT {linha}")

if __name__ == "__main__":
    desbloquear_ips()
