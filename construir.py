# Construye las paginas de LNX TV Player para Google Play y AdMob (hosting gratis: GitHub Pages, repo LNXDEVELOPER26.github.io).
# Se cambia el texto o el correo aqui y se vuelve a ejecutar:  python construir.py
# Formato de los textos: "## " = titulo, "- " = punto de lista, linea en blanco = otro parrafo.
import html
import os
import re

RAIZ = os.path.dirname(os.path.abspath(__file__))
APP = 'LNX TV Player'
FECHA = '3 de noviembre de 2026'
CONTACTO = ''   # el correo de contacto que se ve en las paginas; vacio: no sale la linea
PUB = 'pub-2873519479118996'   # el editor de AdMob (app-ads.txt)

PRIVACIDAD = '''
## Qué es
LNX TV Player reproduce las listas M3U, los enlaces HLS y los videos (MP4 y otros) que tú pegas. No incluye canales, listas ni contenido.

## Lo que se guarda en tu teléfono
Tus listas y enlaces recientes, tus canales favoritos y tus ajustes. No se envían a nuestros servidores. Se borran desde la app o al desinstalarla.

## Lo que recopilamos
- Un identificador de instalación propio de la app, sin relación con tu nombre ni tu correo, para contar cuántos teléfonos la usan y con qué versión.
- Datos técnicos de la conexión, como la dirección IP, que cualquier servidor recibe.
No pedimos nombre, correo, teléfono, ubicación, contactos ni archivos.

## Anuncios
La app muestra anuncios de Google AdMob. Google puede usar el identificador de publicidad de tu dispositivo, tu dirección IP y tus interacciones con los anuncios. Puedes restablecerlo o desactivarlo en Ajustes > Google > Anuncios.
Más información: https://policies.google.com/technologies/partner-sites

## Servidores de terceros
Al abrir una lista, un enlace o un video, la app se conecta directamente a ese servidor, que puede recibir tu dirección IP. No lo controlamos.

## Menores
La app no está dirigida a menores de 13 años.

## Borrar tus datos
Mira la página «Borrar tus datos».

## Cambios
Publicaremos aquí cualquier cambio, con su fecha.
'''

TERMINOS = '''
## Uso
LNX TV Player es un reproductor de video. Al usarlo aceptas estos términos.

## Tu contenido
La app solo reproduce lo que tú agregas. No proporcionamos ni alojamos ese contenido. Tú eres responsable de tener derecho a reproducirlo y de cumplir las leyes de tu país.

## Uso permitido
No uses la app para actividades ilegales ni para dañar a otras personas o servicios.

## Anuncios
La app es gratuita y muestra anuncios.

## Sin garantías
La app se ofrece «tal cual». Que un enlace o una lista se reproduzca depende de servidores que no controlamos.

## Cambios
La versión vigente es la publicada en esta dirección.
'''

BORRADO = '''
## En tu teléfono
- Listas y enlaces recientes: menú (las tres rayas) > «Eliminar listas», o la X de cada una.
- Favoritos: menú > Ajustes > «Borrar mis favoritos».
- Todo: desinstala la app, o en Android entra en Aplicaciones > LNX TV Player > Almacenamiento > «Borrar datos».

## En nuestros servidores
Solo guardamos un contador anónimo de instalaciones, sin nombre ni correo. Si quieres que borremos el dato de tu instalación, escríbenos.

## Publicidad
Los datos de los anuncios los administra Google. Gestiónalos en Ajustes de Android > Google > Anuncios y en https://myadcenter.google.com
'''

PAGINAS = [
    ('privacidad', 'Política de privacidad', PRIVACIDAD, True),
    ('terminos', 'Términos de uso', TERMINOS, False),
    ('borrar-datos', 'Borrar tus datos', BORRADO, False),
]


def esc(t):
    return html.escape(str(t), quote=True)


def enlazar(t):
    t = esc(t)
    t = re.sub(r'(https://[^\s<]+[^\s<.,;:!?)])', r'<a href="\1" rel="noopener">\1</a>', t)
    t = re.sub(r'([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})', r'<a href="mailto:\1">\1</a>', t)
    return t


def a_html(texto):
    salida, lista, parrafo = [], None, []

    def cerrar_parrafo():
        nonlocal parrafo
        if parrafo:
            salida.append('<p>' + '<br>'.join(enlazar(p) for p in parrafo) + '</p>')
            parrafo = []

    def cerrar_lista():
        nonlocal lista
        if lista:
            salida.append('<ul>' + ''.join('<li>' + enlazar(l) + '</li>' for l in lista) + '</ul>')
            lista = None

    for linea in texto.strip().replace('\r\n', '\n').split('\n'):
        l = linea.strip()
        if not l:
            cerrar_parrafo(); cerrar_lista(); continue
        if l.startswith('## '):
            cerrar_parrafo(); cerrar_lista(); salida.append('<h2>' + esc(l[3:]) + '</h2>'); continue
        if l.startswith('- '):
            cerrar_parrafo(); lista = (lista or []) + [l[2:]]; continue
        cerrar_lista(); parrafo.append(l)
    cerrar_parrafo(); cerrar_lista()
    return '\n'.join(salida)


CSS = ('body{margin:0;background:#fff;color:#1c1c1c;font:16px/1.65 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}'
       'main{max-width:760px;margin:0 auto;padding:32px 20px 64px}h1{font-size:28px;line-height:1.25;margin:0 0 4px}'
       'h2{font-size:20px;margin:32px 0 8px}p{margin:0 0 14px}ul{margin:0 0 14px;padding-left:22px}li{margin:4px 0}'
       '.sub{color:#666;font-size:14px;margin:0 0 28px}.pie{margin-top:40px;padding-top:16px;border-top:1px solid #ddd;color:#555;font-size:14px}'
       'a{color:#0b57d0}')


def pagina(titulo, cuerpo, fecha):
    pie = '<div class="pie">Contacto: ' + enlazar(CONTACTO) + '</div>\n' if CONTACTO else ''
    return ('<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<meta name="robots" content="noindex, nofollow">\n'
            '<title>' + esc(titulo + ' · ' + APP) + '</title>\n<style>' + CSS + '</style>\n</head>\n<body>\n<main>\n'
            '<div class="sub">' + esc(APP) + '</div>\n<h1>' + esc(titulo) + '</h1>\n'
            + ('<p class="sub">Última actualización: ' + esc(FECHA) + '</p>\n' if fecha else '')
            + a_html(cuerpo) + '\n' + pie + '</main>\n</body>\n</html>\n')


def escribir(ruta, texto):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8', newline='\n') as f:
        f.write(texto)


for clave, titulo, cuerpo, fecha in PAGINAS:
    escribir(os.path.join(RAIZ, clave, 'index.html'), pagina(titulo, cuerpo, fecha))

# La portada solo lleva a las tres paginas.
indice = ('<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
          '<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="robots" content="noindex, nofollow">\n'
          '<title>' + esc(APP) + '</title>\n<style>' + CSS + '</style>\n</head>\n<body>\n<main>\n<h1>' + esc(APP) + '</h1>\n<ul>\n'
          + ''.join('<li><a href="/' + c + '/">' + esc(t) + '</a></li>\n' for c, t, _, _ in PAGINAS)
          + '</ul>\n</main>\n</body>\n</html>\n')
escribir(os.path.join(RAIZ, 'index.html'), indice)
escribir(os.path.join(RAIZ, 'app-ads.txt'), 'google.com, ' + PUB + ', DIRECT, f08c47fec0942fa0\n')
escribir(os.path.join(RAIZ, '.nojekyll'), '')
print('ok')
