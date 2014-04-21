--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
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
-- Name: results; Type: TABLE; Schema: public; Owner: brent; Tablespace: 
--

CREATE TABLE results (
    updated timestamp with time zone NOT NULL,
    site_id bigint NOT NULL,
    positive_count integer,
    negative_count integer,
    queries integer,
    name text NOT NULL
);


ALTER TABLE public.results OWNER TO brent;

--
-- Name: sites; Type: TABLE; Schema: public; Owner: brent; Tablespace: 
--

CREATE TABLE sites (
    site_id bigint NOT NULL,
    name text NOT NULL,
    url text NOT NULL,
    api_key text,
    notes text,
    quota integer,
    quota_interval interval,
    site_key text,
    class text
);


ALTER TABLE public.sites OWNER TO brent;

--
-- Name: results_view; Type: VIEW; Schema: public; Owner: brent
--

CREATE VIEW results_view AS
    SELECT sites.name, results.updated, results.name AS term, results.positive_count, results.negative_count FROM (results JOIN sites ON ((results.site_id = sites.site_id)));


ALTER TABLE public.results_view OWNER TO brent;

--
-- Name: sites_site_id_seq; Type: SEQUENCE; Schema: public; Owner: brent
--

CREATE SEQUENCE sites_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sites_site_id_seq OWNER TO brent;

--
-- Name: sites_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: brent
--

ALTER SEQUENCE sites_site_id_seq OWNED BY sites.site_id;


--
-- Name: terms; Type: TABLE; Schema: public; Owner: brent; Tablespace: 
--

CREATE TABLE terms (
    name text NOT NULL,
    items text[]
);


ALTER TABLE public.terms OWNER TO brent;

--
-- Name: site_id; Type: DEFAULT; Schema: public; Owner: brent
--

ALTER TABLE ONLY sites ALTER COLUMN site_id SET DEFAULT nextval('sites_site_id_seq'::regclass);


--
-- Name: name_key; Type: CONSTRAINT; Schema: public; Owner: brent; Tablespace: 
--

ALTER TABLE ONLY sites
    ADD CONSTRAINT name_key UNIQUE (name);


--
-- Name: results_pkey; Type: CONSTRAINT; Schema: public; Owner: brent; Tablespace: 
--

ALTER TABLE ONLY results
    ADD CONSTRAINT results_pkey PRIMARY KEY (updated, site_id, name);


--
-- Name: sites_pkey; Type: CONSTRAINT; Schema: public; Owner: brent; Tablespace: 
--

ALTER TABLE ONLY sites
    ADD CONSTRAINT sites_pkey PRIMARY KEY (site_id);


--
-- Name: terms_pkey; Type: CONSTRAINT; Schema: public; Owner: brent; Tablespace: 
--

ALTER TABLE ONLY terms
    ADD CONSTRAINT terms_pkey PRIMARY KEY (name);


--
-- Name: results_name_idx; Type: INDEX; Schema: public; Owner: brent; Tablespace: 
--

CREATE INDEX results_name_idx ON results USING btree (name);


--
-- Name: name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: brent
--

ALTER TABLE ONLY results
    ADD CONSTRAINT name_fkey FOREIGN KEY (name) REFERENCES terms(name);


--
-- Name: results_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: brent
--

ALTER TABLE ONLY results
    ADD CONSTRAINT results_site_id_fkey FOREIGN KEY (site_id) REFERENCES sites(site_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: _postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM _postgres;
GRANT ALL ON SCHEMA public TO _postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: results; Type: ACL; Schema: public; Owner: brent
--

REVOKE ALL ON TABLE results FROM PUBLIC;
REVOKE ALL ON TABLE results FROM brent;
GRANT ALL ON TABLE results TO brent;
GRANT INSERT ON TABLE results TO srom_collector;


--
-- Name: sites; Type: ACL; Schema: public; Owner: brent
--

REVOKE ALL ON TABLE sites FROM PUBLIC;
REVOKE ALL ON TABLE sites FROM brent;
GRANT ALL ON TABLE sites TO brent;
GRANT SELECT ON TABLE sites TO srom_collector;


--
-- Name: results_view; Type: ACL; Schema: public; Owner: brent
--

REVOKE ALL ON TABLE results_view FROM PUBLIC;
REVOKE ALL ON TABLE results_view FROM brent;
GRANT ALL ON TABLE results_view TO brent;
GRANT SELECT ON TABLE results_view TO srom_reader;


--
-- Name: terms; Type: ACL; Schema: public; Owner: brent
--

REVOKE ALL ON TABLE terms FROM PUBLIC;
REVOKE ALL ON TABLE terms FROM brent;
GRANT ALL ON TABLE terms TO brent;
GRANT SELECT ON TABLE terms TO srom_collector;


--
-- PostgreSQL database dump complete
--

