import os
import pandas as pd

# Constantes gerais do projeto:
LINER_THICKNESS = 3 #mm. Espessura do Liner;
MINIMIUM_STRUCTURAL_THICKNESS = 5 #mm. Espessura mínima da estrutura;
PAINT_RATE = 20 #m^2/lata 

##Emendas:
# CONSIDERANDO QUE A ESPESSURA DA EMENDA DO TAMPO-COSTADO SERÁ IGUAL AO VALOR DE ESPESSURA DO TAMPO.
LONGITUDINAL_JOINT_EXTERNAL_THICKNESS = 2 #mm. Espessura externa da emenda longitudinal;
CIRCUNFERENCIAL_SHELL_JOINT_WIDTH = 300 #mm. Largura da emenda circunferencial do costado;
CIRCUNFERENCIAL_SHELL_JOINT_THICKNESS = 3 #mm. Espessura da emenda circunferencial do costado;

##Escada:
FIXING_CLIP_LAMINATION_THICKNESS = 5

# Caminhos Globais
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Diretório base do projeto
DATA_DIR = os.path.join(BASE_DIR, "../data")           # Diretório de dados
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")           # Diretório de dados brutos
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")  # Dados tratados

# Arquivos específicos
TAMPO_ELIPTICO_FILE = os.path.join(PROCESSED_DATA_DIR, "tampo_eliptico.xlsx")

# PROPRIEDADE DOS MATEIRIAS

# Propriedade dos Materiais
## Densidade dos laminados:
## Propriedades Gerais - PRFV
D_HLU = 1700 # kg/m^3. Densidade do laminado produzido por Hand Lay-Up;
D_FW= 2000 # kg/m^3. Densidade do laminado produzido por Filament Winding,

## Propriedades Véu de Superfície:
D_VEIL = 1300 #kg/m^3. Densidade do laminado produzido apenas com véu de superfície e resina.
VEIL_THICKNESS = 0.3 #mm. Espessura do véu de superfície por aplicação;

## Propriedades Mecânicas PRFV - Hand Lay-Up
Z = 0.001 # Alongamento máximo admissível, conforme ASME RTP-1 e ASTM D-3299;
U_A = 0.2985
U_C = 0.3128
K_D = 0.84 # Fator de cálculo ASME RTP-1, 3A-310, pág. 25;

## Propriedades Mecânicas PRFV - Filament Winding
E_HLU = 10340 # MPa    - Módulo de elasticidade da estrutura HLU - conf. ASME RTP-1, tab. 2A-3, tipo II;
EF_HLU = 6895 # MPa    - Módulo de elasticidade na flexão da estrutura HLU - conf. ASME RTP-1. tab. 2A-3, tipo II;
S_U = 103 # MPa    - Tensão UTS da estrutura HLU - Conf. ASME RTP-1, tab. 2A-3, tipo II;
S_A = 151 # MPa    - Tensão UTS na flexão da estrutura HLU - Conf. ASME RTP-1, tab. 2A-3, tipo II.
E_FW = 20000 # MPa  -Módulo de Elasticidade da estrutura FW;
EA_FW = 8785 # MPa  - Módulo de Elasticidade Axial da Estrutura F.W. - 60% Vidro / 70° de F.W.;
EF_FW = 11030 # MPa - Módulo de Elasticidade Cincunf. de Flexão da Estrutura F.W. - 60% Vidro / 70° de F.W.;
EFA_FW = 7580 # MPa - Módulo de Elasticidade Axial de Flexão da Estrutura F.W. - 60% Vidro / 70° de F.W.;
S_FW = 200 # MPa    - Tensão UTS Estrutura F.W.;
S_FWA = 105 # MPa  - Tensão UTS Estrutura Axial F.W..

## Propriedades Mecânicas - Outros materiais
E_AC = 200 # GPa    - Módulo de elasticidade do aço carbono.

## Proporções fibra/resina por processo:
### SPRAY-UP
RESIN_SU = 0.7
FIBER_SU = 0.3

### HLU1 - MANTA E RESINA
RESIN_HLU1 = 0.7
FIBER_HLU1 = 0.3

### HLU2 - MANTA, TECIDO E RESINA
RESIN_HLU2 = 0.7
FIBER_HLU2 = 0.3
MANTA_HLU2 = 0.7
TECIDO_HLU2 = 0.3

### FW - FILAMENT WINDING
RESIN_FW = 0.35
FIBER_FW = 0.65

### LAMINADO VÉU
RESIN_VEIL = 0.9
FIBER_VEIL = 0.10

## CATALISAÇÃO:
DMA_PROPORTION = 0.005
COBALT_PROPORTION = 0.01
BPO_PROPORTION = 0.02
MECKP_PROPORTION = 0.05
THINNER_PROPORTION = 0.025
STYRENE_PROPORTION = 0.05

## CONSUMO PINTURA:
CATALYST_CONSUMPTION = 1 #1:1, OU SEJA, UMA LATA DE CATALISADOR PARA UMA LATA DE TINTA
DILUENT_CONSUMPTION = 1 #1:1, OU SEJA, UMA LATA DE DILUENTE PARA UMA LATA DE TINTA

## VALORES DE IMPOSTOS PADRÃO:
IRPJ_RATE = 1.2 #IMPOSTO DE RENDA PESSOA JURÍDICA
CSSL_RATE = 1.08 #CONTRIBUIÇÃO SOCIAL SOBRE O LUCRO LÍQUIDO
PIS_RATE = 0.65 #PROGRAMA DE INTEGRAÇÃO SOCIAL
COFINS_RATE = 3 #CONTRIBUIÇÃO PARA O FINANCIAMENTO DA SEGURIDADE SOCIAL


## Conversão de unidades:
MM_TO_M = 0.001
M_TO_MM = 1000
KGCM3_TO_KGMM3 = 0.001
MPA_TO_KGFMM2 = 0.101972
MM3_TO_M3 = 1e-9
M3_TO_MM3 = 1e9
IN_TO_MM = 25.4
MM2_TO_M2 = 1e-6