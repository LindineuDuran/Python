import re


def extrai_texto(texto, padrao):
    textoNovoRegex = re.compile(padrao)
    textoNovo = textoNovoRegex.search(texto)

    return textoNovo

def testa_regex(texto, padrao):
    x = re.search(padrao, texto)
    if x:
        print("There's a match!")
        print(f'The match is: {x.group(0)!r}')
        print('The span is:', x.span(0))
    else:
        print("There's no match")

    print(x)

def obtem_num_serie(texto):
    numNF = extrai_texto(texto, "Nº (\d{3}).(\d{3}).(\d{3}).")

    if numNF is None:
        numNF = extrai_texto(texto, "NºSÉRIE :(\d{1})\\n(\d{3}).(\d{3}).(\d{3})")

    if numNF is None:
        numNF = extrai_texto(texto, "SÉRIE (\d{1})N° (\d{3}).(\d{3}).(\d{3})")

    if numNF is None:
        numNF = extrai_texto(texto, "SAÍDA(\d{1})\\nN. (\d{9})\\nSÉRIE (\d{1})\\nFOLHA")

    if numNF is None:
        numNF = extrai_texto(texto, "NF-e\\nNº (\d{3}).(\d{3}).(\d{3})\\nSÉRIE:")

    if numNF is not None:
        newNumNF = extrai_texto(numNF.group(), "(\d{3}).(\d{3}).(\d{3})")

        if newNumNF is not None:
            numNF = newNumNF
        else:
            newNumNF = extrai_texto(numNF.group(), "(\d{9})")
            numNF = newNumNF

        if numNF is not None:
            try:
                numNF = int(numNF.group().replace('.', '').replace(',', ''))
            except:
                print('numNF: ', numNF)

    if numNF is None:
        numNF = extrai_texto(texto, "ASSINATURA DO RECEBEDOR(\d{1,6})")

        if numNF is not None:
            newNumNF = extrai_texto(numNF.group(), "(\d{1,6})")
            newNumNF = newNumNF.group(0)

            if newNumNF is not None:
                numNF = newNumNF
            else:
                newNumNF = extrai_texto(numNF.group(), "(\d{1,6})")
                numNF = newNumNF

    if numNF is None:
        numNF = extrai_texto(texto, "(\d{1,6})KTS")

        if numNF is not None:
            newNumNF = extrai_texto(numNF.group(), "(\d{1,6})")
            newNumNF = newNumNF.group(0)

            if newNumNF is not None:
                numNF = newNumNF
            else:
                newNumNF = extrai_texto(numNF.group(), "(\d{1,6})")
                numNF = newNumNF

    print(numNF)

    return numNF


def obtem_cnpj(texto):
    cnpj = extrai_texto(texto, "(\d{1,3}).(\d{3}).(\d{3})/(\d{4})\\n-\\n(\d{2})")

    if cnpj is None:
        cnpj = extrai_texto(texto, "(\d{1,3}).(\d{3}).(\d{3})/(\d{4})-(\d{2})")

    if cnpj is not None:
        cnpj = cnpj.group().replace('\n-\n', '').replace('.', '').replace('-', '').replace('/', '')

    # if cnpj is not None:
    #    cnpj = extrai_texto(cnpj.group(), "(\d{1,3}).(\d{3}).(\d{3})/(\d{4})\\n-\\n(\d{2})|(\d{1,3}).(\d{3}).(\d{3})/(\d{4})-(\d{2})")

    return cnpj


def obtem_chave(texto):
    chave = extrai_texto(
        texto, '(\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4}) (\d{4})')

    if chave is None:
        chave = extrai_texto(
            texto, '(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4}).(\d{4})')

    if chave is None:
        chave = extrai_texto(
            texto, '(\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})  (\d{4})')

    if chave is None:
        chave = extrai_texto(
            texto, '(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})\n(\d{4})')

    if chave is None:
        chave = extrai_texto(texto, '(\d{44})')

    if chave is None:
        chave = extrai_texto(texto, '(\d{24}) (\d{20})')

    if chave is not None:
        chave = chave.group().replace('.', '').replace(' ', '').replace('\n', '')
    else:
        chave = ''

    return chave
