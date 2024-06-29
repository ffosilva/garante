import sys

result_file = open(sys.argv[1], "r")
size_clicks = 0

if len(sys.argv) > 2:
    size_clicks = int(sys.argv[2])

# header = result_file.readline()
i = 0
milliseconds = 0
for line in result_file:
    print("setTimeout(function () {")
    for i in range(size_clicks):
        print("document.getElementById(\"aumentarnumero\").click();")
    
    numeros = map(int, line.strip().split(";"))
    for numero in numeros:
        print("document.getElementById(\"n%02d\").click();" % numero)

    print("document.getElementById(\"colocarnocarrinho\").click();\n}, %d);" % milliseconds)
    i += 1
    milliseconds += 2000


# ""
# setTimeout(function, milliseconds)
