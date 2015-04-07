--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: sodaRoom; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE sodaRoom (
    message character varying(255),
    username character varying(30)
);


ALTER TABLE public.sodaRoom OWNER TO postgres;

--
-- Name: noodleRoom; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE noodleRoom (
    message character varying(255),
    username character varying(30)
);


ALTER TABLE public.noodleRoom OWNER TO postgres;

--
-- Name: pizzaRoom; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE pizzaRoom (
    message character varying(255),
    username character varying(30)
);


ALTER TABLE public.pizzaRoom OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE users (
    id integer NOT NULL,
    username character varying(30),
    password character varying(30),
    pizzaRoomSub character varying(10),
    sodaRoomSub character varying(10),
    noodleRoomSub character varying(10)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Data for Name: sodaRoom; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sodaRoom (message, username) FROM stdin;
userB in the aqua room.	userB
First message	userB
Second message	userB
Third message	userB
I have access to the Soda Room	userC
userC in the Soda Room	userC
Discussing all things soda related	userC
Test Soda Room	userC
\.


--
-- Data for Name: noodleRoom; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY noodleRoom (message, username) FROM stdin;
I am the only user subscribed to the Noodle Room	userC
No one else is in the Noodle Room	userC
Why is this a chat room just for me?	userC
In the Noodle Room	userC
Test Noodle Room	userC
\.


--
-- Data for Name: pizzaRoom; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY pizzaRoom (message, username) FROM stdin;
Inside the Pizza Room.	userA
I can only post in the Pizza Room.	userA
First message.	userA
Second message.	userA
Third message.	userA
userB in the Pizza Room.	userB
userB also has access to the Soda Room.	userB
Soda Room is the best.	userB
I have access to the Pizza Room	userC
inside the Pizza Room	userC
Test Pizza Room	userC
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY users (id, username, password, pizzaRoomSub, sodaRoomSub, noodleRoomSub) FROM stdin;
39	userA	qwer	True	False	False
38	userB	asdf	True	True	False
37	userC	zxcv	True	True	True
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('users_id_seq', 41, true);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

