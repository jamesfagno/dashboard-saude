# =============================================================
# setup.py — Execute UMA VEZ para montar o projeto completo.
# Como usar:  python setup.py
# =============================================================

import os, csv, hashlib, shutil

_BASE          = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJ     = os.path.join(_BASE, "dashboard_saude")
PASTA_DADOS    = os.path.join(PASTA_PROJ, "dados")
PASTA_FRONTEND = os.path.join(PASTA_PROJ, "frontend")

ARQUIVOS_PY       = ["models.py","storage.py","services.py","rules.py",
                      "dashboard.py","main.py","usuarios.py"]
ARQUIVOS_FRONTEND = ["index.html","style.css","app.js"]

PROCEDIMENTOS_SUS = [
    ("301010072","Consulta em Clínica Geral",             75.38),
    ("301010072","Consulta em Cardiologia",               75.38),
    ("301010072","Consulta em Ortopedia",                 75.38),
    ("301010072","Consulta em Neurologia",                75.38),
    ("301010072","Consulta em Ginecologia e Obstetrícia", 75.38),
    ("301010072","Consulta em Pediatria",                 75.38),
    ("301010072","Consulta em Oftalmologia",              75.38),
    ("301010072","Consulta em Dermatologia",              75.38),
    ("301010072","Consulta em Pneumologia",               75.38),
    ("301010072","Consulta em Urologia",                  75.38),
    ("301010072","Consulta em Endocrinologia",            75.38),
    ("301010072","Consulta em Gastroenterologia",         75.38),
    ("301010072","Consulta em Reumatologia",             130.66),
    ("301010072","Consulta em Psiquiatria",              150.76),
    ("301010072","Consulta em Infectologia",              75.38),
    ("301010048","Consulta Odontologia",                  68.19),
    ("301010048","Consulta Psicologia",                   34.32),
    ("301010048","Consulta Fonoaudiologia",               47.11),
    ("301010048","Consulta Nutrição",                     41.66),
]

PACIENTES = [
    (1, "João Carlos Araújo", "1964-09-03", "107.203.311-11", "SUS", 61928728463),
    (2, "Diego Araújo", "1988-12-04", "114.206.322-12", "SUS", 65966629388),
    (3, "João Carlos Oliveira", "1959-08-13", "121.209.333-13", "SUS", 65990801586),
    (4, "Fábio Alves", "2004-03-27", "128.212.344-14", "Hapvida", 65966306997),
    (5, "Rafael Vieira", "1964-12-15", "135.215.355-15", "SUS", 61966722344),
    (6, "Juliana Rodrigues", "1959-04-26", "142.218.366-16", "Particular", 62922448136),
    (7, "Francisca Ribeiro", "1970-11-09", "149.221.377-17", "SulAmérica", 64915831819),
    (8, "Joana Santos", "1973-12-16", "156.224.388-18", "SUS", 65949349722),
    (9, "Karen Alves", "2003-03-18", "163.227.399-19", "SUS", 62998753260),
    (10, "Henrique Gomes", "1947-02-27", "170.230.410-20", "SUS", 62961019678),
    (11, "Giovanna Rocha", "1972-09-23", "177.233.421-21", "SUS", 64957683626),
    (12, "Diego Lima", "2002-12-18", "184.236.432-22", "Hapvida", 62991756179),
    (13, "Fábio Araújo", "1961-12-17", "191.239.443-23", "SUS", 67960929647),
    (14, "Zélia Rocha", "2001-09-26", "198.242.454-24", "Amil", 61953524491),
    (15, "Paulo Henrique Nunes", "1942-11-17", "205.245.465-25", "Particular", 67945935572),
    (16, "Manoel Pinto", "1990-11-19", "212.248.476-26", "Notre Dame", 64938538251),
    (17, "Eliane Figueira", "1997-09-02", "219.251.487-27", "Bradesco Saúde", 61945551614),
    (18, "Paulo Henrique Araújo", "1990-05-12", "226.254.498-28", "Amil", 64988461803),
    (19, "Yasmin Vieira", "1975-10-31", "233.257.509-29", "Particular", 61928566572),
    (20, "Antônia Cruz", "1944-03-23", "240.260.520-30", "SUS", 61994214382),
    (21, "Igor Cardoso", "1977-11-15", "247.263.531-31", "SulAmérica", 62961642594),
    (22, "Larissa Almeida", "1987-06-21", "254.266.542-32", "Particular", 65911540956),
    (23, "Diego Figueira", "1988-03-04", "261.269.553-33", "Particular", 64924972279),
    (24, "Flávia Ferreira", "1980-09-14", "268.272.564-34", "SUS", 64977187530),
    (25, "Leandro Pinto", "1949-07-18", "275.275.575-35", "Hapvida", 64995758349),
    (26, "Antônio Ribeiro", "2008-05-28", "282.278.586-36", "SUS", 65981182864),
    (27, "Alexandre Costa", "1983-11-01", "289.281.597-37", "SUS", 62958718453),
    (28, "Fernanda Souza", "1961-08-10", "296.284.608-38", "SulAmérica", 62921496211),
    (29, "Tatiana Oliveira", "2008-03-27", "303.287.619-39", "Amil", 61927232410),
    (30, "Joana Ferreira", "1963-10-12", "310.290.630-40", "Amil", 65966792612),
    (31, "Fábio Cruz", "2005-06-26", "317.293.641-41", "Notre Dame", 61951837852),
    (32, "Natália Rocha", "1973-07-02", "324.296.652-42", "Bradesco Saúde", 65970597444),
    (33, "Paulo Henrique Pereira", "1945-09-29", "331.299.663-43", "Particular", 62988961459),
    (34, "Rodrigo Pereira", "1940-08-23", "338.302.674-44", "SUS", 62940728046),
    (35, "Leonardo Souza", "1969-08-23", "345.305.685-45", "SUS", 65941944441),
    (36, "Natália Lopes", "1959-03-22", "352.308.696-46", "Amil", 61986644106),
    (37, "Fernanda Moraes", "1982-06-07", "359.311.707-47", "Unimed", 61922660194),
    (38, "Diego Carvalho", "1971-10-14", "366.314.718-48", "Unimed", 67972682989),
    (39, "Diego Rocha", "1997-12-21", "373.317.729-49", "SUS", 62964038913),
    (40, "Sandra Mendes", "1949-10-20", "380.320.740-50", "SUS", 61935529407),
    (41, "Rosilene Carvalho", "1956-06-17", "387.323.751-51", "Particular", 67943528453),
    (42, "Rafael Moraes", "1989-05-16", "394.326.762-52", "SUS", 62997529405),
    (43, "Francisco Pinto", "2007-08-09", "401.329.773-53", "SUS", 61964547971),
    (44, "Helena Alves", "1975-12-24", "408.332.784-54", "SUS", 61960864911),
    (45, "Lucas Lima", "2010-05-05", "415.335.795-55", "Bradesco Saúde", 64966775103),
    (46, "Rosilene Alves", "1966-08-14", "422.338.806-56", "SUS", 62987736262),
    (47, "Gustavo Costa", "1945-02-16", "429.341.817-57", "SUS", 65973993471),
    (48, "José Antônio Soares", "1947-03-10", "436.344.828-58", "SUS", 62989864260),
    (49, "Diego Mendes", "1961-02-06", "443.347.839-59", "Unimed", 62986460539),
    (50, "Rodrigo Barbosa", "1943-07-26", "450.350.850-60", "SulAmérica", 62966267415),
    (51, "Zélia Lima", "1958-04-29", "457.353.861-61", "Hapvida", 64942035886),
    (52, "Eliane Rodrigues", "2000-04-04", "464.356.872-62", "Hapvida", 64971367643),
    (53, "Zélia Cruz", "1946-07-05", "471.359.883-63", "SUS", 67993370583),
    (54, "Francisco Fernandes", "1959-02-14", "478.362.894-64", "Amil", 64927778019),
    (55, "Yasmin Oliveira", "1961-11-30", "485.365.905-65", "Particular", 64931172421),
    (56, "Tatiana Fernandes", "2003-02-12", "492.368.916-66", "Particular", 65997775215),
    (57, "Diego Nunes", "1989-10-03", "499.371.927-67", "Particular", 62928024248),
    (58, "Francisca Figueira", "1949-08-08", "506.374.938-68", "Notre Dame", 65930863865),
    (59, "Patrícia Barbosa", "1958-11-23", "513.377.949-69", "Notre Dame", 64937326368),
    (60, "Isabela Lopes", "1962-07-12", "520.380.960-70", "SUS", 62995132217),
    (61, "Tatiana Lima", "1943-12-15", "527.383.971-71", "SUS", 64927558317),
    (62, "Luzia Helena Araújo", "1979-08-22", "534.386.982-72", "Amil", 67985283645),
    (63, "Raimundo Oliveira", "2001-12-29", "541.389.993-73", "SUS", 65914835614),
    (64, "Karen Fernandes", "1953-04-14", "548.392.1004-74", "Unimed", 61915614174),
    (65, "Daniela Figueira", "1943-07-31", "555.395.1015-75", "Particular", 61943491314),
    (66, "Marcos Vinícius Cruz", "1990-03-25", "562.398.1026-76", "Unimed", 65930743797),
    (67, "Kleber Ferreira", "1955-11-19", "569.401.1037-77", "Unimed", 62934073380),
    (68, "Sandra Pinto", "1976-12-08", "576.404.1048-78", "Hapvida", 61945810056),
    (69, "Igor Nascimento", "1949-09-12", "583.407.1059-79", "Unimed", 62973174945),
    (70, "Manoel Nunes", "1981-04-18", "590.410.1070-80", "Particular", 64940547349),
    (71, "João Carlos Cardoso", "1957-04-29", "597.413.1081-81", "Unimed", 64947393469),
    (72, "Henrique Lima", "1971-07-03", "604.416.1092-82", "Hapvida", 65963643924),
    (73, "Maria das Graças Santos", "1963-06-08", "611.419.1103-83", "SUS", 65945630292),
    (74, "Raimundo Barbosa", "1978-12-26", "618.422.1114-84", "Particular", 64968571795),
    (75, "Lucas Figueira", "1991-09-23", "625.425.1125-85", "SUS", 64915957459),
    (76, "Maria das Graças Soares", "1988-04-21", "632.428.1136-86", "Hapvida", 61958884978),
    (77, "Antônia Cardoso", "1969-08-15", "639.431.1147-87", "SulAmérica", 64999038359),
    (78, "Gustavo Figueira", "1966-12-10", "646.434.1158-88", "Amil", 64999508850),
    (79, "Camila Martins", "2002-07-20", "653.437.1169-89", "Particular", 65927084279),
    (80, "Gabriel Cardoso", "1974-01-05", "660.440.1180-90", "Hapvida", 61992613013),
    (81, "Eliane Fernandes", "1940-01-14", "667.443.1191-91", "Particular", 64938210242),
    (82, "Sandra Vieira", "1994-06-05", "674.446.1202-92", "Hapvida", 64972409658),
    (83, "Giovanna Cardoso", "1959-03-04", "681.449.1213-93", "Amil", 67932775593),
    (84, "Edilson Soares", "1999-07-23", "688.452.1224-94", "Hapvida", 65954988206),
    (85, "Júlio Cruz", "1961-01-26", "695.455.1235-95", "Hapvida", 64940150759),
    (86, "Antônio Silva", "1944-02-23", "702.458.1246-96", "SUS", 67992043803),
    (87, "Rafael Carvalho", "1996-07-01", "709.461.1257-97", "SulAmérica", 61961536717),
    (88, "Eliane Pereira", "1953-03-28", "716.464.1268-98", "Hapvida", 62924305904),
    (89, "Fernanda Ferreira", "2002-06-07", "723.467.1279-99", "Amil", 67916740197),
    (90, "Kleber Santos", "1980-12-13", "730.470.1290-10", "SUS", 67999600766),
    (91, "Renata Figueira", "1979-09-15", "737.473.1301-11", "SulAmérica", 65967276174),
    (92, "Yasmin Ferreira", "2006-09-19", "744.476.1312-12", "Bradesco Saúde", 67944788100),
    (93, "Júlio Rocha", "1964-11-16", "751.479.1323-13", "Amil", 67994120751),
    (94, "André Luís Almeida", "1946-12-13", "758.482.1334-14", "Notre Dame", 64941473195),
    (95, "Camila Costa", "1988-06-16", "765.485.1345-15", "SUS", 61930244148),
    (96, "Lucas Nascimento", "1953-09-16", "772.488.1356-16", "Notre Dame", 61918620650),
    (97, "Flávia Costa", "1988-09-05", "779.491.1367-17", "Bradesco Saúde", 67918357162),
    (98, "Júlio Carvalho", "1974-12-10", "786.494.1378-18", "SulAmérica", 62987267850),
    (99, "Helena Silva", "1971-07-23", "793.497.1389-19", "Particular", 67966240084),
    (100, "Thiago Pereira", "1964-06-26", "800.500.1400-20", "Unimed", 67913895645),
    (101, "Camila Cardoso", "2000-12-05", "807.503.1411-21", "Unimed", 61972732043),
    (102, "Alexandre Fernandes", "1942-06-02", "814.506.1422-22", "Unimed", 65985751409),
    (103, "Francisco Rocha", "1978-06-14", "821.509.1433-23", "SUS", 67934391257),
    (104, "André Luís Martins", "1969-05-14", "828.512.1444-24", "SUS", 67953868501),
    (105, "Renata Figueira", "1974-01-05", "835.515.1455-25", "Particular", 67943859311),
    (106, "Thiago Silva", "2007-03-14", "842.518.1466-26", "Amil", 62956970882),
    (107, "Bruno Oliveira", "2010-02-01", "849.521.1477-27", "Hapvida", 62914164775),
    (108, "Manoel Nunes", "1941-10-29", "856.524.1488-28", "SulAmérica", 61942016960),
    (109, "Thiago Cardoso", "1950-04-06", "863.527.1499-29", "SulAmérica", 61972415804),
    (110, "Renata Ribeiro", "1955-01-20", "870.530.1510-30", "SulAmérica", 65925372341),
    (111, "Edilson Santos", "1991-12-01", "877.533.1521-31", "SUS", 64987282128),
    (112, "Eliane Nascimento", "1957-10-16", "884.536.1532-32", "SUS", 65994187049),
    (113, "Raimundo Nascimento", "2009-04-20", "891.539.1543-33", "Particular", 65926247735),
    (114, "Marcos Vinícius Fernandes", "1978-06-07", "898.542.1554-34", "Hapvida", 64919255216),
    (115, "Maria das Graças Mendes", "1977-09-07", "905.545.1565-35", "Bradesco Saúde", 62968186525),
    (116, "Mariana Figueira", "1981-03-30", "912.548.1576-36", "Notre Dame", 61968450095),
    (117, "Gustavo Soares", "1998-05-10", "919.551.1587-37", "Particular", 65982232344),
    (118, "Giovanna Carvalho", "2005-08-01", "926.554.1598-38", "SulAmérica", 64953258988),
    (119, "Júlio Pinto", "1947-10-10", "933.557.1609-39", "Particular", 67942730796),
    (120, "Karen Barbosa", "1999-12-12", "940.560.1620-40", "Unimed", 64913852048)
]

PROFISSIONAIS = [
    (1, "Dra. Ana Paula Costa", "Clínica Geral", "CRM-GO 11234"),
    (2, "Dr. Ricardo Mendes", "Cardiologia", "CRM-GO 12468"),
    (3, "Dra. Fernanda Lima", "Ginecologia e Obstetrícia", "CRM-GO 13702"),
    (4, "Dr. Carlos Eduardo Rocha", "Ortopedia", "CRM-GO 14936"),
    (5, "Dra. Mariana Souza", "Pediatria", "CRM-GO 16170"),
    (6, "Dr. Paulo Henrique Faria", "Neurologia", "CRM-GO 17404"),
    (7, "Dra. Juliana Ferreira", "Dermatologia", "CRM-GO 18638"),
    (8, "Dr. André Luís Campos", "Psiquiatria", "CRM-GO 19872"),
    (9, "Dr. Beatriz Andrade", "Endocrinologia", "CRM-GO 21106"),
    (10, "Dra. Marcelo Teixeira", "Oftalmologia", "CRM-GO 22340"),
    (11, "Dr. Cristina Borges", "Urologia", "CRM-GO 23574"),
    (12, "Dra. Eduardo Sampaio", "Reumatologia", "CRM-GO 24808"),
    (13, "Dr. Luciana Freitas", "Gastroenterologia", "CRM-GO 26042"),
    (14, "Dra. Roberto Cunha", "Infectologia", "CRM-GO 27276"),
    (15, "Dr. Priscila Moura", "Pneumologia", "CRM-GO 28510")
]

CONSULTAS = [
    (1, 109, 6, "2024-01-06", "Convênio", "Consulta em Neurologia", 320, "realizada"),
    (2, 44, 5, "2024-01-20", "SUS", "Consulta em Pediatria", 75.38, "realizada"),
    (3, 72, 1, "2024-01-17", "Convênio", "Consulta em Clínica Geral", 185, "realizada"),
    (4, 93, 7, "2024-01-16", "Convênio", "Consulta em Dermatologia", 232, "realizada"),
    (5, 83, 12, "2024-01-16", "Convênio", "Consulta em Reumatologia", 304, "realizada"),
    (6, 38, 4, "2024-01-13", "Convênio", "Consulta em Ortopedia", 304, "realizada"),
    (7, 61, 9, "2024-01-17", "SUS", "Consulta em Endocrinologia", 75.38, "realizada"),
    (8, 46, 12, "2024-01-15", "SUS", "Consulta em Reumatologia", 130.66, "realizada"),
    (9, 30, 2, "2024-01-24", "Convênio", "Consulta em Cardiologia", 281, "realizada"),
    (10, 25, 4, "2024-01-24", "Convênio", "Consulta em Ortopedia", 297, "realizada"),
    (11, 13, 14, "2024-01-07", "SUS", "Consulta em Infectologia", 75.38, "realizada"),
    (12, 23, 5, "2024-01-01", "Particular", "Consulta em Pediatria", 275, "realizada"),
    (13, 7, 9, "2024-01-10", "Convênio", "Consulta em Endocrinologia", 282, "glosada"),
    (14, 82, 14, "2024-01-25", "Convênio", "Consulta em Infectologia", 237, "realizada"),
    (15, 74, 5, "2024-01-16", "Particular", "Consulta em Pediatria", 260, "realizada"),
    (16, 33, 14, "2024-01-16", "Particular", "Consulta em Infectologia", 297, "cancelada"),
    (17, 52, 8, "2024-01-03", "Convênio", "Consulta em Psiquiatria", 420, "realizada"),
    (18, 20, 3, "2024-01-26", "SUS", "Consulta em Ginecologia e Obstetrícia", 75.38, "realizada"),
    (19, 11, 4, "2024-01-04", "SUS", "Consulta em Ortopedia", 75.38, "realizada"),
    (20, 78, 10, "2024-01-26", "Convênio", "Consulta em Oftalmologia", 219, "realizada"),
    (21, 58, 15, "2024-01-15", "Convênio", "Consulta em Pneumologia", 261, "cancelada"),
    (22, 40, 10, "2024-02-20", "SUS", "Consulta em Oftalmologia", 75.38, "realizada"),
    (23, 98, 4, "2024-02-21", "Convênio", "Consulta em Ortopedia", 288, "realizada"),
    (24, 21, 4, "2024-02-06", "Convênio", "Consulta em Ortopedia", 299, "realizada"),
    (25, 53, 8, "2024-02-23", "SUS", "Consulta em Psiquiatria", 150.76, "realizada"),
    (26, 5, 4, "2024-02-10", "SUS", "Consulta em Ortopedia", 75.38, "realizada"),
    (27, 10, 11, "2024-02-08", "SUS", "Consulta em Urologia", 75.38, "glosada"),
    (28, 101, 13, "2024-02-21", "Convênio", "Consulta em Gastroenterologia", 286, "realizada"),
    (29, 55, 2, "2024-02-18", "Particular", "Consulta em Cardiologia", 374, "realizada"),
    (30, 10, 1, "2024-02-06", "SUS", "Consulta em Clínica Geral", 75.38, "realizada"),
    (31, 57, 2, "2024-02-15", "Particular", "Consulta em Cardiologia", 404, "realizada"),
    (32, 65, 9, "2024-02-16", "Particular", "Consulta em Endocrinologia", 368, "realizada"),
    (33, 95, 6, "2024-02-20", "SUS", "Consulta em Neurologia", 75.38, "realizada"),
    (34, 30, 11, "2024-02-27", "Convênio", "Consulta em Urologia", 272, "realizada"),
    (35, 98, 11, "2024-02-27", "Convênio", "Consulta em Urologia", 253, "realizada"),
    (36, 61, 9, "2024-02-21", "SUS", "Consulta em Endocrinologia", 75.38, "realizada"),
    (37, 24, 10, "2024-02-14", "SUS", "Consulta em Oftalmologia", 75.38, "realizada"),
    (38, 12, 8, "2024-02-12", "Convênio", "Consulta em Psiquiatria", 415, "realizada"),
    (39, 110, 3, "2024-02-11", "Convênio", "Consulta em Ginecologia e Obstetrícia", 243, "realizada"),
    (40, 85, 7, "2024-02-27", "Convênio", "Consulta em Dermatologia", 239, "realizada"),
    (41, 12, 6, "2024-02-09", "Convênio", "Consulta em Neurologia", 315, "realizada"),
    (42, 111, 9, "2024-02-27", "SUS", "Consulta em Endocrinologia", 75.38, "glosada"),
    (43, 112, 9, "2024-03-15", "SUS", "Consulta em Endocrinologia", 75.38, "realizada"),
    (44, 67, 6, "2024-03-20", "Convênio", "Consulta em Neurologia", 329, "realizada"),
    (45, 98, 1, "2024-03-07", "Convênio", "Consulta em Clínica Geral", 163, "realizada"),
    (46, 57, 15, "2024-03-23", "Particular", "Consulta em Pneumologia", 361, "realizada"),
    (47, 21, 5, "2024-03-18", "Convênio", "Consulta em Pediatria", 178, "realizada"),
    (48, 29, 14, "2024-03-04", "Convênio", "Consulta em Infectologia", 236, "glosada"),
    (49, 83, 14, "2024-03-05", "Convênio", "Consulta em Infectologia", 237, "glosada"),
    (50, 38, 9, "2024-03-23", "Convênio", "Consulta em Endocrinologia", 268, "realizada"),
    (51, 61, 4, "2024-03-15", "SUS", "Consulta em Ortopedia", 75.38, "realizada"),
    (52, 25, 15, "2024-03-20", "Convênio", "Consulta em Pneumologia", 268, "realizada"),
    (53, 111, 2, "2024-03-09", "SUS", "Consulta em Cardiologia", 75.38, "realizada"),
    (54, 44, 15, "2024-03-26", "SUS", "Consulta em Pneumologia", 75.38, "realizada"),
    (55, 37, 12, "2024-03-10", "Convênio", "Consulta em Reumatologia", 316, "realizada"),
    (56, 111, 3, "2024-03-15", "SUS", "Consulta em Ginecologia e Obstetrícia", 75.38, "realizada"),
    (57, 43, 9, "2024-03-25", "SUS", "Consulta em Endocrinologia", 75.38, "realizada"),
    (58, 120, 6, "2024-03-28", "Convênio", "Consulta em Neurologia", 311, "glosada"),
    (59, 31, 10, "2024-03-13", "Convênio", "Consulta em Oftalmologia", 207, "cancelada"),
    (60, 53, 1, "2024-03-11", "SUS", "Consulta em Clínica Geral", 75.38, "realizada"),
    (61, 50, 11, "2024-03-26", "Convênio", "Consulta em Urologia", 271, "realizada"),
    (62, 64, 1, "2024-03-05", "Convênio", "Consulta em Clínica Geral", 171, "glosada"),
    (63, 43, 14, "2024-03-04", "SUS", "Consulta em Infectologia", 75.38, "cancelada"),
    (64, 57, 2, "2024-03-17", "Particular", "Consulta em Cardiologia", 389, "realizada"),
    (65, 112, 11, "2024-03-05", "SUS", "Consulta em Urologia", 75.38, "realizada"),
    (66, 80, 12, "2024-04-13", "Convênio", "Consulta em Reumatologia", 310, "realizada"),
    (67, 110, 11, "2024-04-28", "Convênio", "Consulta em Urologia", 262, "realizada"),
    (68, 81, 12, "2024-04-25", "Particular", "Consulta em Reumatologia", 411, "cancelada"),
    (69, 5, 10, "2024-04-03", "SUS", "Consulta em Oftalmologia", 75.38, "realizada"),
    (70, 30, 12, "2024-04-03", "Convênio", "Consulta em Reumatologia", 303, "glosada"),
    (71, 98, 11, "2024-04-23", "Convênio", "Consulta em Urologia", 272, "realizada"),
    (72, 89, 5, "2024-04-01", "Convênio", "Consulta em Pediatria", 179, "realizada"),
    (73, 38, 6, "2024-04-12", "Convênio", "Consulta em Neurologia", 318, "realizada"),
    (74, 73, 11, "2024-04-26", "SUS", "Consulta em Urologia", 75.38, "realizada"),
    (75, 11, 10, "2024-04-28", "SUS", "Consulta em Oftalmologia", 75.38, "realizada"),
    (76, 64, 15, "2024-04-19", "Convênio", "Consulta em Pneumologia", 256, "realizada"),
    (77, 59, 5, "2024-04-22", "Convênio", "Consulta em Pediatria", 178, "cancelada"),
    (78, 60, 15, "2024-04-10", "SUS", "Consulta em Pneumologia", 75.38, "realizada"),
    (79, 10, 8, "2024-04-12", "SUS", "Consulta em Psiquiatria", 150.76, "glosada"),
    (80, 39, 11, "2024-04-14", "SUS", "Consulta em Urologia", 75.38, "realizada"),
    (81, 109, 5, "2024-04-07", "Convênio", "Consulta em Pediatria", 190, "cancelada"),
    (82, 14, 4, "2024-04-13", "Convênio", "Consulta em Ortopedia", 300, "realizada"),
    (83, 90, 5, "2024-04-01", "SUS", "Consulta em Pediatria", 75.38, "glosada"),
    (84, 85, 7, "2024-04-09", "Convênio", "Consulta em Dermatologia", 215, "realizada"),
    (85, 117, 10, "2024-04-24", "Particular", "Consulta em Oftalmologia", 291, "cancelada"),
    (86, 100, 13, "2024-05-08", "Convênio", "Consulta em Gastroenterologia", 287, "cancelada"),
    (87, 29, 11, "2024-05-07", "Convênio", "Consulta em Urologia", 264, "realizada"),
    (88, 81, 2, "2024-05-21", "Particular", "Consulta em Cardiologia", 401, "realizada"),
    (89, 75, 6, "2024-05-24", "SUS", "Consulta em Neurologia", 75.38, "realizada"),
    (90, 42, 12, "2024-05-14", "SUS", "Consulta em Reumatologia", 130.66, "realizada"),
    (91, 101, 9, "2024-05-12", "Convênio", "Consulta em Endocrinologia", 276, "realizada"),
    (92, 107, 3, "2024-05-09", "Convênio", "Consulta em Ginecologia e Obstetrícia", 259, "cancelada"),
    (93, 62, 13, "2024-05-10", "Convênio", "Consulta em Gastroenterologia", 291, "cancelada"),
    (94, 103, 2, "2024-05-15", "SUS", "Consulta em Cardiologia", 75.38, "glosada"),
    (95, 19, 13, "2024-05-08", "Particular", "Consulta em Gastroenterologia", 393, "realizada"),
    (96, 47, 2, "2024-05-26", "SUS", "Consulta em Cardiologia", 75.38, "realizada"),
    (97, 69, 2, "2024-05-15", "Convênio", "Consulta em Cardiologia", 286, "realizada"),
    (98, 75, 7, "2024-05-27", "SUS", "Consulta em Dermatologia", 75.38, "realizada"),
    (99, 14, 11, "2024-05-08", "Convênio", "Consulta em Urologia", 260, "realizada"),
    (100, 118, 10, "2024-05-08", "Convênio", "Consulta em Oftalmologia", 220, "realizada"),
    (101, 117, 12, "2024-05-10", "Particular", "Consulta em Reumatologia", 421, "realizada"),
    (102, 5, 5, "2024-05-16", "SUS", "Consulta em Pediatria", 75.38, "realizada"),
    (103, 114, 9, "2024-05-05", "Convênio", "Consulta em Endocrinologia", 272, "realizada"),
    (104, 76, 12, "2024-05-24", "Convênio", "Consulta em Reumatologia", 294, "cancelada"),
    (105, 84, 2, "2024-05-27", "Convênio", "Consulta em Cardiologia", 290, "realizada"),
    (106, 89, 6, "2024-06-07", "Convênio", "Consulta em Neurologia", 319, "realizada"),
    (107, 110, 6, "2024-06-04", "Convênio", "Consulta em Neurologia", 326, "realizada"),
    (108, 8, 7, "2024-06-09", "SUS", "Consulta em Dermatologia", 75.38, "realizada"),
    (109, 109, 14, "2024-06-15", "Convênio", "Consulta em Infectologia", 224, "realizada"),
    (110, 7, 13, "2024-06-11", "Convênio", "Consulta em Gastroenterologia", 275, "glosada"),
    (111, 101, 10, "2024-06-07", "Convênio", "Consulta em Oftalmologia", 202, "cancelada"),
    (112, 71, 4, "2024-06-19", "Convênio", "Consulta em Ortopedia", 288, "cancelada"),
    (113, 30, 6, "2024-06-25", "Convênio", "Consulta em Neurologia", 309, "realizada"),
    (114, 36, 14, "2024-06-05", "Convênio", "Consulta em Infectologia", 226, "realizada"),
    (115, 15, 11, "2024-06-28", "Particular", "Consulta em Urologia", 321, "realizada"),
    (116, 76, 6, "2024-06-01", "Convênio", "Consulta em Neurologia", 310, "realizada"),
    (117, 95, 7, "2024-06-17", "SUS", "Consulta em Dermatologia", 75.38, "realizada"),
    (118, 61, 8, "2024-06-25", "SUS", "Consulta em Psiquiatria", 150.76, "realizada"),
    (119, 58, 9, "2024-06-08", "Convênio", "Consulta em Endocrinologia", 290, "realizada"),
    (120, 59, 11, "2024-06-01", "Convênio", "Consulta em Urologia", 246, "glosada"),
    (121, 109, 7, "2024-06-14", "Convênio", "Consulta em Dermatologia", 236, "realizada"),
    (122, 10, 15, "2024-06-03", "SUS", "Consulta em Pneumologia", 75.38, "realizada"),
    (123, 9, 3, "2024-06-09", "SUS", "Consulta em Ginecologia e Obstetrícia", 75.38, "realizada"),
    (124, 77, 9, "2024-07-10", "Convênio", "Consulta em Endocrinologia", 274, "realizada"),
    (125, 13, 13, "2024-07-23", "SUS", "Consulta em Gastroenterologia", 75.38, "realizada"),
    (126, 56, 8, "2024-07-08", "Particular", "Consulta em Psiquiatria", 556, "realizada"),
    (127, 54, 12, "2024-07-04", "Convênio", "Consulta em Reumatologia", 300, "realizada"),
    (128, 48, 3, "2024-07-22", "SUS", "Consulta em Ginecologia e Obstetrícia", 75.38, "glosada"),
    (129, 9, 2, "2024-07-27", "SUS", "Consulta em Cardiologia", 75.38, "realizada"),
    (130, 13, 12, "2024-07-24", "SUS", "Consulta em Reumatologia", 130.66, "realizada"),
    (131, 72, 1, "2024-07-19", "Convênio", "Consulta em Clínica Geral", 185, "realizada"),
    (132, 86, 2, "2024-07-14", "SUS", "Consulta em Cardiologia", 75.38, "realizada"),
    (133, 112, 15, "2024-07-24", "SUS", "Consulta em Pneumologia", 75.38, "realizada"),
    (134, 77, 5, "2024-07-12", "Convênio", "Consulta em Pediatria", 181, "realizada"),
    (135, 20, 11, "2024-07-16", "SUS", "Consulta em Urologia", 75.38, "realizada"),
    (136, 45, 14, "2024-07-18", "Convênio", "Consulta em Infectologia", 233, "realizada"),
    (137, 74, 4, "2024-07-26", "Particular", "Consulta em Ortopedia", 397, "cancelada"),
    (138, 99, 14, "2024-07-20", "Particular", "Consulta em Infectologia", 329, "realizada"),
    (139, 119, 11, "2024-07-27", "Particular", "Consulta em Urologia", 364, "realizada"),
    (140, 90, 13, "2024-07-10", "SUS", "Consulta em Gastroenterologia", 75.38, "glosada"),
    (141, 45, 1, "2024-07-06", "Convênio", "Consulta em Clínica Geral", 182, "realizada"),
    (142, 9, 3, "2024-07-24", "SUS", "Consulta em Ginecologia e Obstetrícia", 75.38, "realizada"),
    (143, 12, 12, "2024-07-17", "Convênio", "Consulta em Reumatologia", 296, "realizada"),
    (144, 44, 3, "2024-07-12", "SUS", "Consulta em Ginecologia e Obstetrícia", 75.38, "realizada"),
    (145, 73, 10, "2024-08-03", "SUS", "Consulta em Oftalmologia", 75.38, "cancelada"),
    (146, 20, 3, "2024-08-25", "SUS", "Consulta em Ginecologia e Obstetrícia", 75.38, "realizada"),
    (147, 35, 8, "2024-08-22", "SUS", "Consulta em Psiquiatria", 150.76, "realizada"),
    (148, 54, 5, "2024-08-07", "Convênio", "Consulta em Pediatria", 202, "realizada"),
    (149, 56, 2, "2024-08-10", "Particular", "Consulta em Cardiologia", 403, "realizada"),
    (150, 86, 5, "2024-08-02", "SUS", "Consulta em Pediatria", 75.38, "realizada"),
    (151, 1, 4, "2024-08-10", "SUS", "Consulta em Ortopedia", 75.38, "glosada"),
    (152, 99, 3, "2024-08-25", "Particular", "Consulta em Ginecologia e Obstetrícia", 316, "realizada"),
    (153, 64, 12, "2024-08-14", "Convênio", "Consulta em Reumatologia", 295, "realizada"),
    (154, 65, 9, "2024-08-27", "Particular", "Consulta em Endocrinologia", 382, "cancelada"),
    (155, 10, 7, "2024-08-28", "SUS", "Consulta em Dermatologia", 75.38, "realizada"),
    (156, 3, 8, "2024-08-03", "SUS", "Consulta em Psiquiatria", 150.76, "cancelada"),
    (157, 74, 7, "2024-08-19", "Particular", "Consulta em Dermatologia", 305, "realizada"),
    (158, 15, 7, "2024-08-01", "Particular", "Consulta em Dermatologia", 300, "realizada"),
    (159, 118, 6, "2024-08-03", "Convênio", "Consulta em Neurologia", 318, "cancelada"),
    (160, 32, 7, "2024-08-19", "Convênio", "Consulta em Dermatologia", 227, "realizada"),
    (161, 112, 5, "2024-08-24", "SUS", "Consulta em Pediatria", 75.38, "realizada"),
    (162, 100, 3, "2024-08-03", "Convênio", "Consulta em Ginecologia e Obstetrícia", 246, "realizada"),
    (163, 116, 13, "2024-08-12", "Convênio", "Consulta em Gastroenterologia", 279, "realizada"),
    (164, 31, 2, "2024-08-05", "Convênio", "Consulta em Cardiologia", 283, "realizada"),
    (165, 98, 13, "2024-08-21", "Convênio", "Consulta em Gastroenterologia", 270, "realizada"),
    (166, 60, 13, "2024-08-19", "SUS", "Consulta em Gastroenterologia", 75.38, "realizada"),
    (167, 88, 15, "2024-08-19", "Convênio", "Consulta em Pneumologia", 272, "realizada"),
    (168, 111, 11, "2024-08-11", "SUS", "Consulta em Urologia", 75.38, "realizada")
]

PAGAMENTOS = [
    (1, 1, "2024-01-08", 320, "convênio"),
    (2, 2, "2024-01-22", 75.38, "SUS"),
    (3, 3, "2024-01-18", 185, "convênio"),
    (4, 4, "2024-01-19", 232, "convênio"),
    (5, 5, "2024-01-16", 304, "convênio"),
    (6, 6, "2024-01-15", 304, "convênio"),
    (7, 7, "2024-01-19", 75.38, "SUS"),
    (8, 8, "2024-01-17", 130.66, "SUS"),
    (9, 9, "2024-01-25", 281, "convênio"),
    (10, 10, "2024-01-26", 297, "convênio"),
    (11, 11, "2024-01-09", 75.38, "SUS"),
    (12, 12, "2024-01-03", 275, "pix"),
    (13, 14, "2024-01-25", 237, "convênio"),
    (14, 15, "2024-01-17", 260, "pix"),
    (15, 17, "2024-01-03", 420, "convênio"),
    (16, 18, "2024-01-28", 75.38, "SUS"),
    (17, 19, "2024-01-07", 75.38, "SUS"),
    (18, 20, "2024-01-29", 219, "convênio"),
    (19, 22, "2024-02-20", 75.38, "SUS"),
    (20, 23, "2024-02-21", 288, "convênio"),
    (21, 24, "2024-02-06", 299, "convênio"),
    (22, 25, "2024-02-25", 150.76, "SUS"),
    (23, 26, "2024-02-13", 75.38, "SUS"),
    (24, 28, "2024-02-22", 286, "convênio"),
    (25, 29, "2024-02-20", 374, "pix"),
    (26, 30, "2024-02-08", 75.38, "SUS"),
    (27, 31, "2024-02-18", 404, "cartão"),
    (28, 32, "2024-02-16", 368, "cartão"),
    (29, 33, "2024-02-20", 75.38, "SUS"),
    (30, 34, "2024-02-27", 272, "convênio"),
    (31, 35, "2024-02-28", 253, "convênio"),
    (32, 36, "2024-02-23", 75.38, "SUS"),
    (33, 37, "2024-02-17", 75.38, "SUS"),
    (34, 38, "2024-02-12", 415, "convênio"),
    (35, 39, "2024-02-13", 243, "convênio"),
    (36, 40, "2024-03-01", 239, "convênio"),
    (37, 41, "2024-02-12", 315, "convênio"),
    (38, 43, "2024-03-16", 75.38, "SUS"),
    (39, 44, "2024-03-23", 329, "convênio"),
    (40, 45, "2024-03-09", 163, "convênio"),
    (41, 46, "2024-03-24", 361, "dinheiro"),
    (42, 47, "2024-03-18", 178, "convênio"),
    (43, 50, "2024-03-26", 268, "convênio"),
    (44, 51, "2024-03-18", 75.38, "SUS"),
    (45, 52, "2024-03-21", 268, "convênio"),
    (46, 53, "2024-03-12", 75.38, "SUS"),
    (47, 54, "2024-03-26", 75.38, "SUS"),
    (48, 55, "2024-03-13", 316, "convênio"),
    (49, 56, "2024-03-17", 75.38, "SUS"),
    (50, 57, "2024-03-28", 75.38, "SUS"),
    (51, 60, "2024-03-14", 75.38, "SUS"),
    (52, 61, "2024-03-27", 271, "convênio"),
    (53, 64, "2024-03-18", 389, "cartão"),
    (54, 65, "2024-03-07", 75.38, "SUS"),
    (55, 66, "2024-04-15", 310, "convênio"),
    (56, 67, "2024-04-30", 262, "convênio"),
    (57, 69, "2024-04-05", 75.38, "SUS"),
    (58, 71, "2024-04-24", 272, "convênio"),
    (59, 72, "2024-04-01", 179, "convênio"),
    (60, 73, "2024-04-15", 318, "convênio"),
    (61, 74, "2024-04-27", 75.38, "SUS"),
    (62, 75, "2024-04-29", 75.38, "SUS"),
    (63, 76, "2024-04-21", 256, "convênio"),
    (64, 78, "2024-04-11", 75.38, "SUS"),
    (65, 80, "2024-04-17", 75.38, "SUS"),
    (66, 82, "2024-04-15", 300, "convênio"),
    (67, 84, "2024-04-09", 215, "convênio"),
    (68, 87, "2024-05-08", 264, "convênio"),
    (69, 88, "2024-05-24", 401, "pix"),
    (70, 89, "2024-05-26", 75.38, "SUS"),
    (71, 90, "2024-05-15", 130.66, "SUS"),
    (72, 91, "2024-05-14", 276, "convênio"),
    (73, 95, "2024-05-11", 393, "dinheiro"),
    (74, 96, "2024-05-28", 75.38, "SUS"),
    (75, 97, "2024-05-17", 286, "convênio"),
    (76, 98, "2024-05-29", 75.38, "SUS"),
    (77, 99, "2024-05-10", 260, "convênio"),
    (78, 100, "2024-05-11", 220, "convênio"),
    (79, 101, "2024-05-11", 421, "pix"),
    (80, 102, "2024-05-17", 75.38, "SUS"),
    (81, 103, "2024-05-08", 272, "convênio"),
    (82, 105, "2024-05-29", 290, "convênio"),
    (83, 106, "2024-06-08", 319, "convênio"),
    (84, 107, "2024-06-06", 326, "convênio"),
    (85, 108, "2024-06-09", 75.38, "SUS"),
    (86, 109, "2024-06-15", 224, "convênio"),
    (87, 113, "2024-06-25", 309, "convênio"),
    (88, 114, "2024-06-06", 226, "convênio"),
    (89, 115, "2024-06-30", 321, "pix"),
    (90, 116, "2024-06-02", 310, "convênio"),
    (91, 117, "2024-06-17", 75.38, "SUS"),
    (92, 118, "2024-06-25", 150.76, "SUS"),
    (93, 119, "2024-06-10", 290, "convênio"),
    (94, 121, "2024-06-17", 236, "convênio"),
    (95, 122, "2024-06-04", 75.38, "SUS"),
    (96, 123, "2024-06-11", 75.38, "SUS"),
    (97, 124, "2024-07-13", 274, "convênio"),
    (98, 125, "2024-07-24", 75.38, "SUS"),
    (99, 126, "2024-07-11", 556, "cartão"),
    (100, 127, "2024-07-06", 300, "convênio"),
    (101, 129, "2024-07-30", 75.38, "SUS"),
    (102, 130, "2024-07-25", 130.66, "SUS"),
    (103, 131, "2024-07-21", 185, "convênio"),
    (104, 132, "2024-07-17", 75.38, "SUS"),
    (105, 133, "2024-07-26", 75.38, "SUS"),
    (106, 134, "2024-07-13", 181, "convênio"),
    (107, 135, "2024-07-16", 75.38, "SUS"),
    (108, 136, "2024-07-20", 233, "convênio"),
    (109, 138, "2024-07-20", 329, "dinheiro"),
    (110, 139, "2024-07-28", 364, "cartão"),
    (111, 141, "2024-07-09", 182, "convênio"),
    (112, 142, "2024-07-24", 75.38, "SUS"),
    (113, 143, "2024-07-20", 296, "convênio"),
    (114, 144, "2024-07-14", 75.38, "SUS"),
    (115, 146, "2024-08-25", 75.38, "SUS"),
    (116, 147, "2024-08-25", 150.76, "SUS"),
    (117, 148, "2024-08-09", 202, "convênio"),
    (118, 149, "2024-08-13", 403, "dinheiro"),
    (119, 150, "2024-08-02", 75.38, "SUS"),
    (120, 152, "2024-08-25", 316, "pix"),
    (121, 153, "2024-08-15", 295, "convênio"),
    (122, 155, "2024-08-31", 75.38, "SUS"),
    (123, 157, "2024-08-22", 305, "cartão"),
    (124, 158, "2024-08-04", 300, "dinheiro"),
    (125, 160, "2024-08-22", 227, "convênio"),
    (126, 161, "2024-08-26", 75.38, "SUS"),
    (127, 162, "2024-08-04", 246, "convênio"),
    (128, 163, "2024-08-13", 279, "convênio"),
    (129, 164, "2024-08-06", 283, "convênio"),
    (130, 165, "2024-08-24", 270, "convênio"),
    (131, 166, "2024-08-22", 75.38, "SUS"),
    (132, 167, "2024-08-21", 272, "convênio"),
    (133, 168, "2024-08-11", 75.38, "SUS")
]

USUARIOS = [
    (1, "admin",    "Administrador",     "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9", "admin"),
    (2, "gestor1",  "Gestor Financeiro", "18f2b94d784d03c222cb7c47148cdb8457f1ef3eaf3e317711f25d55747f6a35", "gestor"),
    (3, "recepcao", "Recepção",           "8c61c48211844338cea877a63bec62b4a89ccb68870fe1e00e71dda89c56a36c", "operador"),
]


def _csv(caminho, colunas, linhas):
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(colunas)
        w.writerows(linhas)

def main():
    print()
    print("=" * 54)
    print("  SETUP — Dashboard Gestão em Saúde")
    print("=" * 54)

    print()
    for pasta in [PASTA_PROJ, PASTA_DADOS, PASTA_FRONTEND]:
        os.makedirs(pasta, exist_ok=True)
        print(f"  ✔ {os.path.relpath(pasta, _BASE)}/")

    print()
    _csv(os.path.join(PASTA_DADOS,"pacientes.csv"),
         ["id","nome","data_nascimento","cpf","convenio","telefone"], PACIENTES)
    print(f"  ✔ pacientes.csv        ({len(PACIENTES)} registros)")

    _csv(os.path.join(PASTA_DADOS,"profissionais.csv"),
         ["id","nome","especialidade","crm"], PROFISSIONAIS)
    print(f"  ✔ profissionais.csv    ({len(PROFISSIONAIS)} registros)")

    _csv(os.path.join(PASTA_DADOS,"procedimentos.csv"),
         ["codigo_sigtap","descricao","valor_sus_2024"], PROCEDIMENTOS_SUS)
    print(f"  ✔ procedimentos.csv    ({len(PROCEDIMENTOS_SUS)} procedimentos)")

    _csv(os.path.join(PASTA_DADOS,"consultas.csv"),
         ["id","paciente_id","profissional_id","data","tipo","procedimento","valor","status"],
         CONSULTAS)
    print(f"  ✔ consultas.csv        ({len(CONSULTAS)} registros — Jan a Ago/2024)")

    _csv(os.path.join(PASTA_DADOS,"pagamentos.csv"),
         ["id","consulta_id","data_pagamento","valor_pago","forma"], PAGAMENTOS)
    print(f"  ✔ pagamentos.csv       ({len(PAGAMENTOS)} registros)")

    _csv(os.path.join(PASTA_DADOS,"usuarios.csv"),
         ["id","login","nome","senha_hash","perfil"], USUARIOS)
    print(f"  ✔ usuarios.csv         ({len(USUARIOS)} usuários)")

    print()
    for nome in ARQUIVOS_PY:
        origem  = os.path.join(_BASE, nome)
        destino = os.path.join(PASTA_PROJ, nome)
        if os.path.exists(origem):
            shutil.copy2(origem, destino)
            print(f"  ✔ {nome}")
        else:
            print(f"  ⚠ {nome}  ← não encontrado, copie manualmente")

    print()
    for nome in ARQUIVOS_FRONTEND:
        origem  = os.path.join(_BASE, nome)
        destino = os.path.join(PASTA_FRONTEND, nome)
        if os.path.exists(origem):
            shutil.copy2(origem, destino)
            print(f"  ✔ {nome}")
        else:
            print(f"  ⚠ {nome}  ← não encontrado, copie manualmente")

    print("""
  ┌──────────────────────────────────────────────┐
  │  Usuários criados                            │
  │  login      senha          perfil            │
  │  ─────────  ────────────── ────────────────  │
  │  admin      admin123       Administrador     │
  │  gestor1    gestor123      Gestor            │
  │  recepcao   recepcao1      Operador          │
  └──────────────────────────────────────────────┘

  Próximos passos:
  1. cd dashboard_saude
  2. python main.py
  3. No menu → opção 6  (gera dados.json)
  4. Abrir o front-end:
     cd frontend
     python -m http.server 8000
     Acesse: http://localhost:8000
""")
    print("=" * 54)
    print("  Setup concluído!")
    print("=" * 54)
    print()

if __name__ == "__main__":
    main()
