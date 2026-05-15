from datetime import date

from sqlalchemy import (
    String,
    Integer,
    Date,
    SmallInteger,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


from db import Base

class Df5(Base):
    """
    Дані про трудові відносини, професію, посаду та періоди роботи фізичної особи.
    Імовірно використовується у звітності ЄСВ / ПФУ / кадровому обліку.
    """

    __tablename__ = "df5s"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    PERIOD_M: Mapped[int | None] = mapped_column(
        SmallInteger,
        nullable=True,
        comment="Звітний місяць"
    )

    PERIOD_Y: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Звітний рік"
    )

    UKR_GROMAD: Mapped[int | None] = mapped_column(
        SmallInteger,
        nullable=True,
        comment="Ознака громадянства України"
    )

    NUMIDENT: Mapped[str | None] = mapped_column(
        String(10),
        index=True,
        nullable=True,
        comment="Ідентифікаційний номер особи"
    )

    LN: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Прізвище"
    )

    NM: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Ім’я"
    )

    FTN: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="По батькові"
    )

    START_DT: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Дата початку трудових відносин"
    )

    END_DT: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Дата завершення трудових відносин"
    )

    ZO: Mapped[int | None] = mapped_column(
        SmallInteger,
        nullable=True,
        comment="Код категорії застрахованої особи"
    )

    PID_ZV: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        comment="Підстава або ідентифікатор звільнення"
    )

    NRM_DT: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Дата наказу або нормативного документа"
    )

    DOG_CPH: Mapped[int | None] = mapped_column(
        SmallInteger,
        nullable=True,
        comment="Ознака цивільно-правового договору"
    )

    PNR: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
        comment="Назва професії або робіт"
    )

    PROF: Mapped[str | None] = mapped_column(
        String(6),
        nullable=True,
        comment="Код професії"
    )

    POS: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
        comment="Назва посади"
    )

    PID: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
        comment="Підстава прийняття або кадровий документ"
    )

    VZV: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
        comment="Вид зайнятості або відносин"
    )

    VS: Mapped[int | None] = mapped_column(
        SmallInteger,
        nullable=True,
        comment="Ознака військової служби або спецстатусу"
    )

    PIR: Mapped[int | None] = mapped_column(
        SmallInteger,
        nullable=True,
        comment="Ознака пільги або спеціального режиму"
    )

    OZN: Mapped[str | None] = mapped_column(
        String(1),
        nullable=True,
        comment="Службова ознака запису"
    )