from decimal import Decimal
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Numeric


class Df1(SQLModel, table=True):
    __tablename__ = "df1s"

    id: int | None = Field(default=None, primary_key=True)

    PERIOD_M: int | None = Field(default=None, index=True)
    PERIOD_Y: int | None = Field(default=None, index=True)
    UKR_GROMAD: int | None = None
    ST: int | None = None

    NUMIDENT: str | None = Field(default=None, max_length=10, index=True)

    LN: str | None = Field(default=None, max_length=100, index=True)
    NM: str | None = Field(default=None, max_length=100, index=True)
    FTN: str | None = Field(default=None, max_length=100)

    ZO: int | None = None
    PAY_TP: int | None = None
    PAY_MNTH: int | None = None
    PAY_YEAR: int | None = None

    SUM_TOTAL: Decimal | None = Field(
        default=None,
        sa_column=Column(Numeric(16, 2))
    )

    SUM_MAX: Decimal | None = Field(
        default=None,
        sa_column=Column(Numeric(16, 2))
    )

    SUM_INS: Decimal | None = Field(
        default=None,
        sa_column=Column(Numeric(16, 2))
    )

    OTK: int | None = None
    EXP: int | None = None
    KD_NP: int | None = None
    KD_NZP: int | None = None
    KD_PTV: int | None = None
    NRM: int | None = None
    KD_VP: int | None = None

    SUM_DIFF: Decimal | None = Field(
        default=None,
        sa_column=Column(Numeric(16, 2))
    )

    SUM_NARAH: Decimal | None = Field(
        default=None,
        sa_column=Column(Numeric(16, 2))
    )

    NRC: int | None = None

    OZN: str | None = Field(default=None, max_length=1)
    OTD: str | None = Field(default=None, max_length=1)

    SYS_ERROR: str | None = Field(default=None, max_length=2000)