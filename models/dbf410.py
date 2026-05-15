from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import (
    Integer,
    String,
    Numeric,
    Date,
)
from sqlalchemy.orm import Mapped, mapped_column

from db import Base

class Df4(Base):
    """
    Дані таблиці dBase III Plus.

    Містить інформацію про:
    - звітний період
    - фізичну особу
    - доходи
    - податки
    - дати прийняття / звільнення
    - податкові ознаки
    """

    __tablename__ = "df4s"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Внутрішній ID запису"
    )

    NP: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        index=True,
        comment="Порядковий номер запису"
    )

    PERIOD: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        index=True,
        comment="Місяць звітного періоду"
    )

    RIK: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        index=True,
        comment="Рік звітного періоду"
    )

    KOD: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="",
        index=True,
        comment="Код або службовий ідентифікатор запису"
    )

    TYP: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        index=True,
        comment="Тип запису"
    )

    TIN: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="",
        index=True,
        comment="РНОКПП / ІПН фізичної особи"
    )

    S_NAR: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
        default=Decimal("0.00"),
        comment="Сума нарахованого доходу"
    )

    S_DOX: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
        default=Decimal("0.00"),
        comment="Сума виплаченого доходу"
    )

    S_TAXN: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
        default=Decimal("0.00"),
        comment="Сума нарахованого податку"
    )

    S_TAXP: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
        default=Decimal("0.00"),
        comment="Сума перерахованого податку"
    )

    OZN_DOX: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        index=True,
        comment="Ознака доходу"
    )

    D_PRIYN: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        index=True,
        comment="Дата прийняття працівника"
    )

    D_ZVILN: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        index=True,
        comment="Дата звільнення працівника"
    )

    OZN_PILG: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        index=True,
        comment="Ознака податкової пільги"
    )

    OZNAKA: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="",
        index=True,
        comment="Додаткова службова ознака"
    )

    A051: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
        default=Decimal("0.00"),
        comment="Додаткове числове поле A051"
    )

    A05: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
        default=Decimal("0.00"),
        comment="Додаткове числове поле A05"
    )

    def __repr__(self) -> str:
        return (
            f"DfRow("
            f"id={self.id}, "
            f"tin='{self.TIN}', "
            f"rik={self.RIK}, "
            f"period={self.PERIOD}"
            f")"
        )