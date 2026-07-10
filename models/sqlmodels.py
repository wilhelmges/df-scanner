from decimal import Decimal
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Numeric
from typing import Optional
from datetime import date


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

class Df4(SQLModel, table=True):
    __tablename__ = "df4s"

    id: Optional[int] = Field(default=None, primary_key=True)

    NP: Optional[int] = None
    PERIOD: Optional[int] = None
    RIK: Optional[int] = None

    KOD: str = Field(max_length=10)
    TYP: Optional[int] = None
    TIN: str = Field(max_length=10)

    S_NAR: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(12, 2))
    )
    S_DOX: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(12, 2))
    )
    S_TAXN: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(12, 2))
    )
    S_TAXP: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(12, 2))
    )

    OZN_DOX: Optional[int] = None

    D_PRIYN: Optional[date] = None
    D_ZVILN: Optional[date] = None

    OZN_PILG: Optional[int] = None

    OZNAKA: str = Field(max_length=1)

    A051: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(12, 2))
    )
    A05: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(Numeric(12, 2))
    )

class Df5(SQLModel, table=True):
    __tablename__ = "df5s"

    id: Optional[int] = Field(default=None, primary_key=True)

    PERIOD_M: Optional[int] = None
    PERIOD_Y: Optional[int] = None

    UKR_GROMAD: Optional[int] = None

    NUMIDENT: Optional[str] = Field(default=None, max_length=10)

    LN: Optional[str] = Field(default=None, max_length=100)
    NM: Optional[str] = Field(default=None, max_length=100)
    FTN: Optional[str] = Field(default=None, max_length=100)

    START_DT: Optional[date] = None
    END_DT: Optional[date] = None

    ZO: Optional[int] = None

    PID_ZV: Optional[str] = Field(default=None, max_length=150)

    NRM_DT: Optional[date] = None

    DOG_CPH: Optional[int] = None

    PNR: Optional[str] = Field(default=None, max_length=250)

    PROF: Optional[str] = Field(default=None, max_length=6)

    POS: Optional[str] = Field(default=None, max_length=250)

    PID: Optional[str] = Field(default=None, max_length=250)

    VZV: Optional[str] = Field(default=None, max_length=250)

    VS: Optional[int] = None

    PIR: Optional[int] = None

    OZN: Optional[str] = Field(default=None, max_length=1)