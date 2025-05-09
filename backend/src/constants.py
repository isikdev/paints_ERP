import re
import uuid
import datetime
from enum import Enum
from typing import Final

class DosageTypeEnum(Enum):
    percent_binder = 'percent_binder'
    percent_amount = 'percent_amount'
    absolute = 'absolute'


DocumentTypes: Final = [
    {'name': 'Base Recipe', 'direction': 0},
    {'name': 'Recipe', 'direction': 0},
    {'name': 'Receipt', 'direction': 1},
    {'name': 'ShipmentReturn', 'direction': 1},
    {'name': 'Shipment', 'direction': -1},
    {'name': 'ReceiptReturn', 'direction': -1},
    {'name': 'NomenclatureIssue', 'direction': -1},
    {'name': 'ProductionReport', 'direction': 1},
    {'name': 'Complectation', 'direction': 0},
    {'name': 'InitialStockSetting', 'direction': 1},
]


class DocumentTypesEnum(str, Enum):
    BaseRecipeType = 'Base Recipe'
    RecipeType = 'Recipe'
    Receipt = 'Receipt'
    Shipment = 'Shipment'
    ProductionReport = 'ProductionReport'



class DocumentStatuses(str, Enum):
    Registered = 'Registered'
    Posted = 'Posted'
    SetToDeletion = 'SetToDeletion'


NAME_MATCH_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[A-Za-zА-Яа-яЁё][A-Za-zА-Яа-яЁё0-9 ,.\-_\"()]+$")
MAX_NAME_LENGTH: Final = 100

STATUS_NAME_MAX_LENGTH: Final = 10

STANDARD_MEASURE_UNITS = [
    {"id": uuid.uuid4(), "name": "Единица",            "short_name": "ед"},
    {"id": uuid.uuid4(), "name": "Киловатт",           "short_name": "кВт"},
    {"id": uuid.uuid4(), "name": "Килограмм",          "short_name": "кг"},
    {"id": uuid.uuid4(), "name": "Литр",               "short_name": "л"},
    {"id": uuid.uuid4(), "name": "Метр",               "short_name": "м"},
    {"id": uuid.uuid4(), "name": "Квадратный метр",    "short_name": "м2"},
    {"id": uuid.uuid4(), "name": "Кубический метр",    "short_name": "м3"},
    {"id": uuid.uuid4(), "name": "Месяц",              "short_name": "мес"},
    {"id": uuid.uuid4(), "name": "Погонный метр",      "short_name": "пог. м"},
    {"id": uuid.uuid4(), "name": "Рулон",              "short_name": "рул"},
    {"id": uuid.uuid4(), "name": "Сутки",              "short_name": "сут"},
    {"id": uuid.uuid4(), "name": "Тонна",              "short_name": "т"},
    {"id": uuid.uuid4(), "name": "Тысяча штук",        "short_name": "тыс. шт"},
    {"id": uuid.uuid4(), "name": "Упаковка",           "short_name": "упак"},
    {"id": uuid.uuid4(), "name": "Час",                "short_name": "ч"},
    {"id": uuid.uuid4(), "name": "Человеко‑час",       "short_name": "чел. ч"},
    {"id": uuid.uuid4(), "name": "Штука",              "short_name": "шт"},
    {"id": uuid.uuid4(), "name": "Ящик",               "short_name": "ящ"},
]

STANDARD_NOMENCLATURE_TYPES = [
    {"id": uuid.uuid4(), "name": "Товары"},
    {"id": uuid.uuid4(), "name": "Услуги"},
    {"id": uuid.uuid4(), "name": "Топливо"},
    {"id": uuid.uuid4(), "name": "Сырье"},
    {"id": uuid.uuid4(), "name": "Продукция"},
    {"id": uuid.uuid4(), "name": "Полуфабрикаты"},
    {"id": uuid.uuid4(), "name": "Оборудование"},
    {"id": uuid.uuid4(), "name": "Материалы"},
    {"id": uuid.uuid4(), "name": "Малоценное оборудование и запасы"},
    {"id": uuid.uuid4(), "name": "Инвентарь и хозяйственные принадлежности"},
    {"id": uuid.uuid4(), "name": "Возвратная тара"},
]

ROOT_LKM_ID = uuid.uuid4()
PROD_LKM_ID = uuid.uuid4()
GOODS_ID    = uuid.uuid4()

STANDARD_NOMENCLATURE_GROUPS = [
    {"id": ROOT_LKM_ID,  "parent_id": None,          "name": "Сырьё ПРОИЗВОДСТВО"},
    {"id": PROD_LKM_ID,  "parent_id": None,          "name": "Продукция ЛКМ"},
    {"id": GOODS_ID,     "parent_id": None,          "name": "Товары"},
    {"id": uuid.uuid4(), "parent_id": ROOT_LKM_ID,   "name": "Пленкообразователи"},
    {"id": uuid.uuid4(), "parent_id": ROOT_LKM_ID,   "name": "Пигменты"},
    {"id": uuid.uuid4(), "parent_id": ROOT_LKM_ID,   "name": "Наполнители"},
    {"id": uuid.uuid4(), "parent_id": ROOT_LKM_ID,   "name": "Сиккативы"},
    {"id": uuid.uuid4(), "parent_id": ROOT_LKM_ID,   "name": "Диспергаторы"},
    {"id": uuid.uuid4(), "parent_id": ROOT_LKM_ID,   "name": "Реологические добавки"},
    {"id": uuid.uuid4(), "parent_id": ROOT_LKM_ID,   "name": "Антипленкообразователи"},
    {"id": uuid.uuid4(), "parent_id": ROOT_LKM_ID,   "name": "Растворители"},
]

_TYPE_IDS: Final = {
    nt["name"]: nt["id"] for nt in STANDARD_NOMENCLATURE_TYPES
}
_GROUP_IDS: Final = {
    g["name"]: g["id"] for g in STANDARD_NOMENCLATURE_GROUPS
}
_UNIT_IDS: Final = {
    mu["name"]: mu["id"] for mu in STANDARD_MEASURE_UNITS
}

NOMENCLATURES = [
    {
        "id": uuid.uuid4(), "name": "Эмаль ПФ-115",
        "description": "",         "type_id": _TYPE_IDS["Продукция"],
        "group_id": _GROUP_IDS["Продукция ЛКМ"],         "measure_unit_id": _UNIT_IDS["Килограмм"],
        "properties": {"color": ["белый"]},
    },
    {
        "id": uuid.uuid4(), "name": "Лак ПФ-060",
        "description": "",         "type_id": _TYPE_IDS["Сырье"],
        "group_id": _GROUP_IDS["Пленкообразователи"],    "measure_unit_id": _UNIT_IDS["Килограмм"],
        "properties": {"solids_content": 53, "density": 1.2},
    },
    {
        "id": uuid.uuid4(), "name": "Лак ПФ-060 для белой эмали",
        "description": "Для светлых эмалей",             "type_id": _TYPE_IDS["Сырье"],
        "group_id": _GROUP_IDS["Пленкообразователи"],    "measure_unit_id": _UNIT_IDS["Килограмм"],
        "properties": {"solids_content": 53, "density": 1.2},
    },
    {
        "id": uuid.uuid4(), "name": "Диоксид титана пигментный TIOx-280",
        "description": "",         "type_id": _TYPE_IDS["Сырье"],
        "group_id": _GROUP_IDS["Пигменты"],    "measure_unit_id": _UNIT_IDS["Килограмм"],
        "properties": {"density": 4.1, "oil_absorption": 25},
    },
    {
        "id": uuid.uuid4(), "name": "Кальцид LinCarb-2xk",
        "description": "",         "type_id": _TYPE_IDS["Сырье"],
        "group_id": _GROUP_IDS["Наполнители"],    "measure_unit_id": _UNIT_IDS["Килограмм"],
        "properties": {"density": 1.15, "oil_absorption": 16},
    },
    {
        "id": uuid.uuid4(), "name": "Добавка Attdry 69",
        "description": "",         "type_id": _TYPE_IDS["Сырье"],
        "group_id": _GROUP_IDS["Сиккативы"],             "measure_unit_id": _UNIT_IDS["Килограмм"],
        "properties": {"percent_binder": 0.0001, "drier_group": "I", "metal_content": 0.15},
    },
    {
        "id": uuid.uuid4(), "name": "Pangel B20",
        "description": "",         "type_id": _TYPE_IDS["Сырье"],
        "group_id": _GROUP_IDS["Реологические добавки"], "measure_unit_id": _UNIT_IDS["Килограмм"],
        "properties": {"percent_amount": 0.005},
    },
    {
        "id": uuid.uuid4(), "name": "Лецитин соевый жидкий",
        "description": "",         "type_id": _TYPE_IDS["Сырье"],
        "group_id": _GROUP_IDS["Диспергаторы"],          "measure_unit_id": _UNIT_IDS["Килограмм"],
        "properties": {},
    },
    {
        "id": uuid.uuid4(), "name": "Лецитин соевый «Ханицитин»",
        "description": "",         "type_id": _TYPE_IDS["Сырье"],
        "group_id": _GROUP_IDS["Диспергаторы"],          "measure_unit_id": _UNIT_IDS["Килограмм"],
        "properties": {},
    },
    {
        "id": uuid.uuid4(), "name": "Уайт-спирит",
        "description": "",         "type_id": _TYPE_IDS["Сырье"],
        "group_id": _GROUP_IDS["Растворители"],          "measure_unit_id": _UNIT_IDS["Килограмм"],
        "properties": {},
    },
    {
        "id": uuid.uuid4(), "name": "МЕКО",
        "description": "",         "type_id": _TYPE_IDS["Сырье"],
        "group_id": _GROUP_IDS["Антипленкообразователи"],"measure_unit_id": _UNIT_IDS["Килограмм"],
        "properties": {"percent_amount": 0.004},
    },
]

_NOM_IDS: Final = {
    nom["name"]: nom["id"] for nom in NOMENCLATURES
}


RULES_EXAMPLE: Final[dict] = {
    "film_former_part": {
      "materials": [
          {
              'uuids': [_NOM_IDS['Лак ПФ-060']],
              'ratios': [1],
              'dosage': None
          },
          {
              'uuids': [_NOM_IDS['Лак ПФ-060 для белой эмали']],
              'ratios': [1],
              'dosage': None
          }
      ]
    },

    "pigment_part": [
      {
        "color": "Белый",
        "materials": [
          {
            "nomenclature_group_id": _GROUP_IDS['Пигменты'],
            "items": [
                {
                  'uuids': [_NOM_IDS['Диоксид титана пигментный TIOx-280']],
                  'ratios': [1],
                  'dosage': None
                }
            ]
          },
          {
            "nomenclature_group_id": _GROUP_IDS['Наполнители'],
            "items": [
                {
                  'uuids': [_NOM_IDS['Кальцид LinCarb-2xk']],
                  'ratios': [1],
                  'dosage': None
                }
            ]
          },
          {
            "nomenclature_group_id": _GROUP_IDS['Пленкообразователи'],
            "items": [
                {
                  'uuids': [_NOM_IDS['Лак ПФ-060 для белой эмали']],
                  'ratios': [1],
                  'dosage': None
                }
            ]
          }
        ],
        "dry_residue": 0.65,
        "pigmentation_degree": 2,
        "filler_ratio": 3
      },
      {
        "color": "black",
        "materials": [
          {
            "nomenclature_group_id": _GROUP_IDS['Пигменты'],
            "items": [
                {
                  'uuids': [_NOM_IDS['Диоксид титана пигментный TIOx-280']],
                  'ratios': [1],
                  'dosage': None
                }
            ]
          },
          {
            "nomenclature_group_id": _GROUP_IDS['Наполнители'],
            "items": [
                {
                  'uuids': [_NOM_IDS['Кальцид LinCarb-2xk']],
                  'ratios': [1],
                  'dosage': None
                }
            ]
          },
          {
            "nomenclature_group_id": _GROUP_IDS['Пленкообразователи'],
            "items": [
                {
                  'uuids': [_NOM_IDS['Лак ПФ-060 для белой эмали']],
                  'ratios': [1],
                  'dosage': None
                }
            ]
          }
        ],
        "dry_residue": 0.65,
        "pigmentation_degree": 2,
        "filler_ratio": 3
      }
    ],

    "additives_part": {
      "materials": [
        {
          "nomenclature_group_id": _GROUP_IDS['Сиккативы'],
          "items": [
              {
                  'uuids': [_NOM_IDS['Добавка Attdry 69']],
                  'ratios': [1],
                  'dosage': {'percent_amount': 0.001}
               }
          ]
        },
        {
          "nomenclature_group_id": _GROUP_IDS['Диспергаторы'],
          "items": [
              {
                  'uuids': [_NOM_IDS['Лецитин соевый жидкий']],
                  'ratios': [1],
                  'dosage': None
               }
          ]
        },
        {
          "nomenclature_group_id": _GROUP_IDS['Реологические добавки'],
          "items": [
              {
                  'uuids': [_NOM_IDS['Pangel B20']],
                  'ratios': [1],
                  'dosage': None
               }
          ]
        },
        {
          "nomenclature_group_id": _GROUP_IDS['Антипленкообразователи'],
          "items": [
              {
                  'uuids': [_NOM_IDS['МЕКО']],
                  'ratios': [1],
                  'dosage': None
               }
          ]
        }
      ]
    },

    "solvent_part": {
      "materials": [
        {
          'uuids': [_NOM_IDS['Уайт-спирит']],
          'ratios': [1],
          'dosage': None
        }
      ]
    },

    "is_posted": True
  }

BASE_RECIPE_BODY_EXAMPLE: Final[dict] = {
  "status": "Posted",
  "document_datetime": datetime.datetime.now(),
  "commentary": "Example commentary",
  "rules": RULES_EXAMPLE,
  "name": 'ПФ-115'
}
