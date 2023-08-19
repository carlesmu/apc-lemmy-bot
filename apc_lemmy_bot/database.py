# -*- coding: utf-8 -*-
#    Copyright (C) 2023  Carles Muñoz Gorriz <carlesmu@internautas.org>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""apc_lemmy_bot database module."""

import datetime
import random
import urllib.request

from typing import List, Optional
from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as saorm
from sqlalchemy_utils import database_exists

from apc_lemmy_bot import apc_lb_conf, __version__
from apc_lemmy_bot.event import Event


class Base(saorm.DeclarativeBase):  # pylint: disable=R0903  # Too few public methods
    """Declarative base class for the database tables."""


class Info(Base):  # pylint: disable=R0903  # Too few public methods
    """Declarative class for the **info** table."""

    __tablename__ = "info"

    id_int: saorm.Mapped[int] = saorm.mapped_column(primary_key=True)
    key: saorm.Mapped[str] = saorm.mapped_column(
        sa.String(30), index=True, unique=True, nullable=False
    )
    value: saorm.Mapped[str] = saorm.mapped_column(sa.String(200))

    def __repr__(self) -> str:
        return f"<Info>(id_int={self.id_int!r}, key={self.key!r}, value={self.value!r}"


class Events(Base):  # pylint: disable=R0903  # Too few public methods
    """Declarative class for the **events** table."""

    __tablename__ = "events"

    id_int: saorm.Mapped[int] = saorm.mapped_column(primary_key=True)
    id_uuid: saorm.Mapped[UUID] = saorm.mapped_column(
        index=True, unique=True, nullable=False
    )
    slugTitle: saorm.Mapped[str] = saorm.mapped_column(
        index=True, unique=True, nullable=False
    )
    date: saorm.Mapped[datetime.date] = saorm.mapped_column(index=True)
    month: saorm.Mapped[int] = saorm.mapped_column(sa.SmallInteger)
    day: saorm.Mapped[int] = saorm.mapped_column(sa.SmallInteger)
    langcode: saorm.Mapped[str] = saorm.mapped_column(sa.String(2))
    title: saorm.Mapped[str]
    otd: saorm.Mapped[str]
    description: saorm.Mapped[str]
    NSFW: saorm.Mapped[bool]

    # Add composed index:
    __table_args__ = (sa.Index("monthDay", "month", "day"),)

    images: saorm.Mapped[List["Images"]] = saorm.relationship(
        # back_populates="Events",
        primaryjoin="and_(Events.id_int==Images.event_id_int,"
        "Events.id_uuid==Images.event_id_uuid)",
        backref="event",
    )

    links: saorm.Mapped[List["Links"]] = saorm.relationship(
        # back_populates="event",
        primaryjoin="and_(Events.id_int==Links.event_id_int,"
        "Events.id_uuid==Links.event_id_uuid)",
        backref="event",
    )

    tags: saorm.Mapped[List["Tags"]] = saorm.relationship(
        # back_populates="Events",
        primaryjoin="and_(Events.id_int==Tags.event_id_int,"
        "Events.id_uuid==Tags.event_id_uuid)",
        backref="event",
    )

    extended: saorm.Mapped["EventsExtended"] = saorm.relationship(
        # back_populates="Events",
        primaryjoin="and_(Events.id_int==EventsExtended.event_id_int,"
        "Events.id_uuid==EventsExtended.event_id_uuid)",
        backref="event",
    )

    posted: saorm.Mapped[List["EventsPosted"]] = saorm.relationship(
        # back_populates="Events",
        primaryjoin="and_(Events.id_int==EventsPosted.event_id_int,"
        "Events.id_uuid==EventsPosted.event_id_uuid)",
        backref="event",
    )

    def __repr__(self) -> str:
        return f"<Events>(id_uuid={self.id_uuid!r}, slugTitle={self.slugTitle!r} ...)"


class Images(Base):  # pylint: disable=R0903  # Too few public methods
    """Declarative class for the **images** table."""

    __tablename__ = "images"

    id_int: saorm.Mapped[int] = saorm.mapped_column(primary_key=True)
    event_id_int = saorm.mapped_column(sa.ForeignKey("events.id_int"))
    event_id_uuid = saorm.mapped_column(sa.ForeignKey("events.id_uuid"))
    img: saorm.Mapped[sa.LargeBinary] = saorm.mapped_column(
        sa.LargeBinary, nullable=True
    )
    imgSrc: saorm.Mapped[str] = saorm.mapped_column(nullable=True)
    imgAltText: saorm.Mapped[str] = saorm.mapped_column(nullable=True)

    def __repr__(self) -> str:
        return (
            f"<Images>("
            f"event_id_uuid={self.event_id_uuid!r}, img={bool(self.img)!r}, "
            f"imgSrc={self.imgSrc!r}, imgAltText={self.imgAltText!r})"
        )


class Links(Base):  # pylint: disable=R0903  # Too few public methods
    """Declarative class for the **links** table."""

    __tablename__ = "links"

    id_int: saorm.Mapped[int] = saorm.mapped_column(primary_key=True)
    event_id_int = saorm.mapped_column(sa.ForeignKey("events.id_int"))
    event_id_uuid = saorm.mapped_column(sa.ForeignKey("events.id_uuid"))
    link: saorm.Mapped[str]

    def __repr__(self) -> str:
        return f"<Links>(" f"event_id_uuid={self.event_id_uuid!r}, link={self.link!r})"


class Tags(Base):  # pylint: disable=R0903  # Too few public methods
    """Declarative class for the **tags** table."""

    __tablename__ = "tags"

    id_int: saorm.Mapped[int] = saorm.mapped_column(primary_key=True)
    event_id_int = saorm.mapped_column(sa.ForeignKey("events.id_int"))
    event_id_uuid = saorm.mapped_column(sa.ForeignKey("events.id_uuid"))
    tag: saorm.Mapped[str]

    def __repr__(self) -> str:
        return f"<Tags>(" f"event_id_uuid={self.event_id_uuid!r}, tag={self.tag!r})"


class EventsExtended(Base):  # pylint: disable=R0903  # Too few public methods
    """Declarative class for the **events_extended** table."""

    __tablename__ = "events_extended"

    id_int: saorm.Mapped[int] = saorm.mapped_column(primary_key=True)

    # We use unique = try in the foreigns keys to force a 1 to 1 relation
    event_id_int = saorm.mapped_column(sa.ForeignKey("events.id_int"), unique=True)
    event_id_uuid = saorm.mapped_column(sa.ForeignKey("events.id_uuid"), unique=True)
    base_event_url: saorm.Mapped[str] = saorm.mapped_column(nullable=True)
    event_url: saorm.Mapped[str] = saorm.mapped_column(nullable=True)
    base_event_img_url: saorm.Mapped[str] = saorm.mapped_column(nullable=True)
    img_url: saorm.Mapped[str] = saorm.mapped_column(nullable=True)
    first_stored_date: saorm.Mapped[datetime.date] = saorm.mapped_column(nullable=True)
    first_stored_timestamp: saorm.Mapped[datetime.datetime] = saorm.mapped_column(
        nullable=True
    )
    stored_date: saorm.Mapped[datetime.date] = saorm.mapped_column(nullable=True)
    stored_timestamp: saorm.Mapped[datetime.datetime] = saorm.mapped_column(
        nullable=True
    )
    apc_version: saorm.Mapped[str]

    def __repr__(self) -> str:
        return (
            f"<EventsExtended>("
            f"event_id_uuid={self.event_id_uuid!r}, "
            f"apc_version={self.apc_version!r}, event_url={self.event_url!r}, "
            f"img_url={self.img_url!r}, "
            f"first_stored_timestamp={self.first_stored_timestamp!r}, "
            f"stored_timestamp={self.stored_timestamp!r})"
        )


class EventsPosted(Base):  # pylint: disable=R0903  # Too few public methods
    """Declarative class for the **events_posted** table."""

    __tablename__ = "events_posted"

    id_int: saorm.Mapped[int] = saorm.mapped_column(primary_key=True)

    event_id_int = saorm.mapped_column(sa.ForeignKey("events.id_int"))
    event_id_uuid = saorm.mapped_column(sa.ForeignKey("events.id_uuid"))

    url: saorm.Mapped[str] = saorm.mapped_column(nullable=True, unique=True)
    date: saorm.Mapped[datetime.date] = saorm.mapped_column(nullable=True)
    timestamp: saorm.Mapped[datetime.datetime] = saorm.mapped_column(nullable=True)

    def __repr__(self) -> str:
        return (
            f"<EventsPosted>("
            f"event_id_uuid={self.event_id_uuid!r}, "
            f"url={self.url!r}, date={self.date!r}, timestamp={self.timestamp!r})"
        )


class Database:
    """Main class of the database module."""

    database_url: str
    engine: sa.Engine
    metadata: sa.MetaData

    def __init__(
        self,
        database_url: Optional[str] = apc_lb_conf.database,
        echo: Optional[bool] = True,
    ):
        """Initialize a database object.

        Parameters
        ----------
        database_url : Optional[str], optional
            The database url. The default is `apc_lb_conf.database`.
        echo : Optional[bool], optional
            It will be passed to the engine. The default is True.
        """
        if database_url:
            apc_lb_conf.database = database_url
        self.database_url = apc_lb_conf.database
        self.engine = sa.create_engine(self.database_url, echo=echo)
        self.metadata = Base.metadata
        if not database_exists(self.database_url):
            self.create_database()

    def create_database(self) -> None:
        """Create the database.

        Returns
        -------
        None

        """
        self.metadata.create_all(self.engine)
        with saorm.sessionmaker(self.engine)() as session:
            for key, value in [
                ("apl_lemmy_bot_version", f"{__version__}"),
                ("creation_date", f"{datetime.datetime.today()}"),
                ("last_change", f"{datetime.datetime.today()}"),
            ]:
                info: Info = Info(key=key, value=value)
                session.add(info)
            session.commit()

    @classmethod
    def _update_last_change(cls, session: saorm.Session) -> None:
        """Update the *extended.last_change* row.

        Parameters
        ----------
        session : saorm.Session
            A active session.

        Returns
        -------
        None
        """
        last_change = session.execute(
            sa.select(Info).filter_by(key="last_change")
        ).scalar_one()
        last_change.value = f"{datetime.datetime.today()}"

    @classmethod
    def _get_event_from_view(cls, view: Events) -> Event:
        """Create a apc_lemmy_bot.Event from a view/row.

        Parameters
        ----------
        view : Events
            The view/row used to create the event.

        Returns
        -------
        Event
            The apc_lemmy_bot.Event object created.
        """
        img_src: Optional[str] = None
        img_alt_txt: Optional[str] = None

        if view.images:
            img_src = view.images[0].imgSrc if view.images[0] else None
            img_alt_txt = view.images[0].imgAltText if view.images[0] else None

        return Event(
            {
                "id": str(view.id_uuid),
                "title": view.title,
                "slugTitle": view.slugTitle,
                "otd": view.otd,
                "description": view.description,
                "imgSrc": img_src,
                "imgAltText": img_alt_txt,
                "NSFW": view.NSFW,
                "date": view.date.strftime("%Y-%m-%d"),
                "links": [x.link for x in view.links],
                "tags": [x.tag for x in view.tags],
                "day": view.day,
                "month": view.month,
                "langcode": view.langcode,
            },
            base_event_url=view.extended.base_event_url,
            base_event_img_url=view.extended.base_event_img_url,
        )

    @classmethod
    def _create_view_from_event(cls, event: Event) -> Events:
        """Create a view/row of a event.

        Parameters
        ----------
        event : Event
            An event object.

        Returns
        -------
        Events
            A view/row of the event.
        """
        view = Events(
            id_uuid=UUID(event.id),
            title=event.title,
            slugTitle=event.slugTitle,
            otd=event.otd,
            description=event.description,
            NSFW=event.NSFW,
            date=event.date,
            month=event.month,
            day=event.day,
            langcode=event.langcode,
        )

        img_url_: Optional[str] = event.get_image_url()
        img_url: str = img_url_ if img_url_ else ""

        view.extended = EventsExtended(
            apc_version=f"{__version__}",
            base_event_url=event.base_event_url,
            event_url=event.get_event_url(),
            base_event_img_url=event.base_event_img_url,
            img_url=img_url,
            first_stored_date=datetime.date.today(),
            first_stored_timestamp=datetime.datetime.today(),
            stored_date=datetime.date.today(),
            stored_timestamp=datetime.datetime.today(),
        )

        _img = None
        if event.imgSrc:
            req = urllib.request.Request(
                img_url,
                data=None,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 "
                        "Safari/537.36"
                    )
                },
            )

            # Some times we get this error:
            # urllib.error.URLError: <urlopen error [SSL:CERTIFICATE_VERIFY_FAILED]
            # certificate verify failed: unable to get local issuer certificate
            try:
                with urllib.request.urlopen(req) as response:
                    _img = response.read()
            except urllib.error.URLError as err:
                print(f"Warning: Error {err}. We try again ...")
                with urllib.request.urlopen(req) as response:
                    _img = response.read()

        if event.imgAltText or _img:
            view.images.append(
                Images(img=_img, imgSrc=event.imgSrc, imgAltText=event.imgAltText)
            )

        for _link in event.links:
            view.links.append(Links(link=_link))
        for _tag in event.tags:
            view.tags.append(Tags(tag=_tag))

        return view

    def _insert_event_view(self, view: Events) -> None:
        """Insert a view/row in the database.

        Parameters
        ----------
        view : Events
            The row to insert in the database.

        Returns
        -------
        None
        """
        with saorm.sessionmaker(self.engine)() as session:
            session.add(view)
            self._update_last_change(session)
            session.commit()

    def _update_event_view(self, view: Events) -> None:
        """Update a view/row in the database.

        Parameters
        ----------
        view : Events
            The row to insert in the database.

        Returns
        -------
        None
        """
        with saorm.sessionmaker(self.engine)() as session:
            session.add(view)
            self._update_last_change(session)
            session.commit()

    def get_views_by_month_day(self, month: int, day: int) -> Optional[List[Events]]:
        with saorm.sessionmaker(self.engine)() as session:
            stmt_uuids = (
                sa.select(Events.id_uuid)
                .where(Events.month == month)
                .where(Events.day == day)
            )
            try:
                uuids = session.scalars(stmt_uuids).all()
            except sa.exc.NoResultFound:
                return None
            if not uuids:
                return None
            ret: list[Events] = []
            for uuid in uuids:
                view = self.get_view_by_id(uuid)
                if view:
                    ret.append(view)
            return ret

    def get_random_dated_event(
        self, views: List[Events], date: datetime.datetime
    ) -> Optional[Event]:
        not_posted_recent = []
        not_posted = []

        for view in views:
            posted_recent = False
            if hasattr(view, "posted") and len(view.posted) > 0:
                for posted in view.posted:
                    if posted.date >= (date - datetime.timedelta(days=100)).date():
                        posted_recent = True
                        continue
            else:
                not_posted.append(view)

            if not posted_recent:
                not_posted_recent.append(view)

        if len(not_posted) > 0:
            return self._get_event_from_view(random.choice(not_posted))
        elif len(not_posted_recent) > 0:
            return self._get_event_from_view(random.choice(not_posted_recent))
        else:
            return None

    def update_posted_event(self, id_uuid: UUID, url) -> None:
        view = self.get_view_by_id(id_uuid)
        timestamp = datetime.datetime.now()

        if view is None:
            raise BaseException(f"View/row not found f{id_uuid}")

        with saorm.sessionmaker(self.engine)() as session:
            session.execute(
                sa.insert(EventsPosted),
                [
                    {
                        "event_id_int": view.id_int,
                        "event_id_uuid": view.id_uuid,
                        "url": url,
                        "date": timestamp.date(),
                        "timestamp": timestamp,
                    }
                ],
            )
            session.commit()

    def get_view_by_id(self, id_uuid: UUID) -> Optional[Events]:
        """Get a the database Event object associated with a id.

        Parameters
        ----------
        id_uuid : UUID
            The *UUID* to look for.

        Returns
        -------
        Tuple[Union[Events | None], Union[Event | None]]
            The event view/row and the event object.
        """
        with saorm.sessionmaker(self.engine)() as session:
            # Event:
            view: Optional[Events] = None

            stmt_events = sa.select(Events).where(Events.id_uuid == id_uuid)
            try:
                view = session.scalars(stmt_events).one()
            except sa.exc.NoResultFound:
                return None
            if not view:
                return None

            # TODO:
            # Without this, I get:
            # sqlalchemy.orm.exc.DetachedInstanceError:
            # Parent instance <Events at 0x7f08f99b4c90> is not bound to a Session;
            # lazy load operation of attribute 'images' cannot proceed (Background on
            # this error at: https://sqlalche.me/e/20/bhk3)
            # pylint: disable=pointless-statement
            view
            view.images,
            view.links,
            view.tags,
            view.extended,
            view.posted

            return view

    def add_event(self, event: Event, silence: bool = True) -> None:
        """Add a event object to the database.

        If it exists and it's not the same that is stored in the database, it updated
        it.

        Parameters
        ----------
        event : Event
            The event to be added.
        silence : bool, optional
            Show information in std output. The default is True.

        Returns
        -------
        None
        """

        def _ignore():
            if not silence:
                print("It was stored. Pass")

        def _update():
            if not silence:
                print("It was stored. Updating")
            view = self._create_view_from_event(event)

            view_from_database.id_uuid = view.id_uuid
            view_from_database.title = view.title
            view_from_database.slugTitle = view.slugTitle
            view_from_database.otd = view.otd
            view_from_database.description = view.description
            view_from_database.NSFW = view.NSFW
            view_from_database.date = view.date
            view_from_database.month = view.month
            view_from_database.day = view.day
            view_from_database.langcode = view.langcode
            view_from_database.images = view.images
            view_from_database.links = view.links
            view_from_database.tags = view.tags

            first_stored_date = view_from_database.extended.first_stored_date
            first_stored_timestamp = view_from_database.extended.first_stored_timestamp

            view_from_database.extended = view.extended
            view_from_database.extended.first_stored_date = first_stored_date
            view_from_database.extended.first_stored_timestamp = first_stored_timestamp

            self._update_event_view(view_from_database)

        def _store():
            if not silence:
                print("It's new. Inserting")
            self._insert_event_view(self._create_view_from_event(event))

        # It's in the database ?
        view_from_database = self.get_view_by_id(UUID(event.id))
        event_from_database = (
            None
            if not view_from_database
            else self._get_event_from_view(view_from_database)
        )

        if event_from_database == event:
            # It was stored
            _ignore()
        elif view_from_database:
            # Stored but with changes -> update:
            _update()
        else:
            # new:
            _store()


def large_binary_to_bytes(val: sa.LargeBinary) -> bytes:
    """Return a binary from a large binary.

    Parameters
    ----------
    val : sa.LargeBinary
        The large binary.

    Returns
    -------
    bytes
        The binary value.

    """
    return bytes(val)
