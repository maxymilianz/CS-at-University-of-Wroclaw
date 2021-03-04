BEGIN;


DROP TABLE IF EXISTS ids CASCADE;
DROP TABLE IF EXISTS members CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS actions CASCADE;
DROP TABLE IF EXISTS votes CASCADE;

CREATE TABLE ids(
	id INT PRIMARY KEY
);

CREATE TABLE members(
	id INT PRIMARY KEY REFERENCES ids(id),
	password VARCHAR NOT NULL,
	leader BOOLEAN NOT NULL DEFAULT FALSE,
	last_activity BIGINT,
	votes_for INT NOT NULL DEFAULT 0,
	votes_against INT NOT NULL DEFAULT 0
);

CREATE TABLE projects(
	id INT PRIMARY KEY REFERENCES ids(id),
	authority_id INT NOT NULL REFERENCES ids(id)
);

CREATE TABLE actions(
	id INT PRIMARY KEY REFERENCES ids(id),
	action_type BOOLEAN NOT NULL,
	project_id INT NOT NULL REFERENCES projects(id),
	member_id INT NOT NULL REFERENCES members(id),
	votes_for INT NOT NULL DEFAULT 0,
	votes_against INT NOT NULL DEFAULT 0
);

CREATE TABLE votes(
	member_id INT NOT NULL REFERENCES members(id),
	action_id INT NOT NULL REFERENCES actions(id),
	vote_type BOOLEAN NOT NULL
);


CREATE OR REPLACE FUNCTION leader(moment BIGINT, password VARCHAR, member INT) RETURNS VARCHAR AS $$
BEGIN
	IF member IN (SELECT id FROM members) THEN
		RETURN 'ERROR';
	ELSE
		INSERT INTO ids VALUES (member);
		INSERT INTO members(id, password, leader, last_activity)
			VALUES (member, crypt(password, gen_salt('md5')), TRUE, moment);
		RETURN 'OK';
	END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_member(last_activity BIGINT, member INT, password VARCHAR) RETURNS VOID AS $$
BEGIN
	INSERT INTO ids VALUES (member);
	INSERT INTO members(id, password, last_activity) VALUES (member, crypt(password, gen_salt('md5')), last_activity);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION is_active(moment BIGINT, member INT) RETURNS BOOLEAN AS $$
BEGIN
RETURN (to_timestamp(moment) - (SELECT to_timestamp(last_activity) FROM members WHERE id = member)) < INTERVAL '1 year'; 
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_action(is_support BOOLEAN, moment BIGINT, member INT, given_password VARCHAR, action INT, project INT, authority INT DEFAULT NULL) RETURNS VARCHAR AS $$
BEGIN
	IF member NOT IN (SELECT id FROM members) THEN
		PERFORM create_member(moment, member, given_password);
	END IF;
	
	IF member IN (SELECT id FROM members WHERE id = member AND members.password = crypt(given_password, members.password) AND is_active(moment, member)) THEN
		IF action IN (SELECT id FROM actions) THEN
			RETURN 'ERROR';
		ELSE
			UPDATE members SET last_activity = moment WHERE id = member;
			
			IF project in (SELECT id FROM projects) THEN
				INSERT INTO ids VALUES (action);
				INSERT INTO actions(id, action_type, project_id, member_id) VALUES (action, is_support, project, member);
			ELSE
				IF authority IS NULL THEN
					RETURN 'ERROR';
				ELSE
					INSERT INTO ids VALUES (project);
					IF authority NOT IN (SELECT authority_id FROM projects) THEN
						INSERT INTO ids VALUES (authority);
					END IF;
					INSERT INTO projects VALUES (project, authority);
					INSERT INTO ids VALUES (action);
					INSERT INTO actions(id, action_type, project_id, member_id) VALUES (action, is_support, project, member);
				END IF;
			END IF;
			
			RETURN 'OK';
		END IF;
	ELSE
		RETURN 'ERROR';
	END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION support(moment BIGINT, member INT, password VARCHAR, action INT, project INT, authority INT DEFAULT NULL) RETURNS VARCHAR AS $$
BEGIN
RETURN (SELECT create_action(TRUE, moment, member, password, action, project, authority));
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION protest(moment BIGINT, member INT, password VARCHAR, action INT, project INT, authority INT DEFAULT NULL) RETURNS VARCHAR AS $$
BEGIN
RETURN (SELECT create_action(FALSE, moment, member, password, action, project, authority));
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION vote(is_upvote BOOLEAN, moment BIGINT, member INT, given_password VARCHAR, action INT) RETURNS VARCHAR AS $$
BEGIN
	IF member NOT IN (SELECT id FROM members) THEN
		PERFORM create_member(moment, member, given_password);
	END IF;
	
	IF member IN (SELECT id FROM members WHERE id = member AND members.password = crypt(given_password, members.password) AND is_active(moment, member)) THEN
		IF action IN (SELECT id FROM actions) THEN
			IF (SELECT COUNT(*) FROM actions WHERE member_id = member AND id = action) = 0 THEN
				UPDATE members SET last_activity = moment WHERE id = member;
				INSERT INTO votes VALUES (member, action, is_upvote);
				
				IF is_upvote THEN
					UPDATE members SET votes_for = votes_for + 1 WHERE members.id = (SELECT member_id FROM actions WHERE actions.id = action);
					UPDATE actions SET votes_for = votes_for + 1 WHERE actions.id = action;
				ELSE
					UPDATE members SET votes_against = votes_against + 1 WHERE members.id = (SELECT member_id FROM actions WHERE actions.id = action);
					UPDATE actions SET votes_against = votes_against + 1 WHERE actions.id = action;
				END IF;
				
				RETURN 'OK';
			ELSE
				RETURN 'ERROR 1';
			END IF;
		ELSE
			RETURN 'ERROR 2';
		END IF;
	ELSE
		RETURN 'ERROR 3';
	END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION upvote(moment BIGINT, member INT, password VARCHAR, action INT) RETURNS VARCHAR AS $$
BEGIN
	RETURN (SELECT vote(TRUE, moment, member, password, action));
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION downvote(moment BIGINT, member INT, password VARCHAR, action INT) RETURNS VARCHAR AS $$
BEGIN
	RETURN (SELECT vote(FALSE, moment, member, password, action));
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_actions(moment BIGINT, member INT, given_password VARCHAR, is_support BOOLEAN DEFAULT NULL, some_id INT DEFAULT NULL) RETURNS TABLE(action INT, action_type BOOLEAN, project INT, authority INT, votes_for INT, votes_against INT) AS $$
BEGIN
	IF member IN (SELECT id FROM members WHERE leader AND members.password = crypt(given_password, members.password)) THEN
		UPDATE members SET last_activity = moment WHERE members.id = member;
		
		RETURN QUERY (SELECT actions.id, actions.action_type, actions.project_id,
					  projects.authority_id, actions.votes_for, actions.votes_against
					  FROM actions JOIN projects ON actions.project_id = projects.id
					  WHERE (is_support IS NULL OR (is_support = actions.action_type))
					  AND (some_id IS NULL OR (some_id IN (SELECT id FROM projects)
					  AND actions.project_id = some_id)
					  OR (some_id IN (SELECT authority_id FROM projects)
					  	  AND projects.authority_id = some_id)) ORDER BY actions.id ASC);
	END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_projects(moment BIGINT, member INT, given_password VARCHAR, authority INT DEFAULT NULL) RETURNS TABLE(project INT, returned_authority INT) AS $$
BEGIN
	IF member IN (SELECT id FROM members WHERE leader AND members.password = crypt(given_password, members.password)) THEN
		UPDATE members SET last_activity = moment WHERE members.id = member;
		
		RETURN QUERY (SELECT id, authority_id FROM projects WHERE authority IS NULL OR
		authority = authority_id ORDER BY projects.id ASC);
	END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_votes(moment BIGINT, member INT, given_password VARCHAR, some_id INT DEFAULT NULL) RETURNS TABLE(returned_member INT, votes_for BIGINT, votes_against BIGINT) AS $$
BEGIN
	IF member IN (SELECT id FROM members WHERE leader AND members.password = crypt(given_password, members.password)) THEN
		UPDATE members SET last_activity = moment WHERE members.id = member;
		
		RETURN QUERY (SELECT members.id,
					  CASE WHEN returned_votes_for IS NULL THEN 0 ELSE returned_votes_for.votes_for END,
					  CASE WHEN against IS NULL THEN 0 ELSE against.votes_against END
					  FROM members LEFT JOIN
					  (SELECT votes.member_id, COUNT(*) AS votes_for FROM votes JOIN
					   actions ON actions.id = votes.action_id WHERE
					   votes.vote_type AND (some_id IS NULL OR
					   (some_id IN (SELECT id FROM actions) AND actions.id = some_id)
					   OR
					   (some_id IN (SELECT id FROM projects) AND actions.project_id = some_id))
					   GROUP BY votes.member_id) returned_votes_for ON members.id = returned_votes_for.member_id LEFT JOIN
					  (SELECT votes.member_id, COUNT(*) AS votes_against FROM votes JOIN
					   actions ON actions.id = votes.action_id WHERE
					   (NOT votes.vote_type) AND (some_id IS NULL OR
					   (some_id IN (SELECT id FROM actions) AND actions.id = some_id)
					   OR
					   (some_id IN (SELECT id FROM projects) AND actions.project_id = some_id))
					   GROUP BY votes.member_id) against ON members.id = against.member_id
					  ORDER BY members.id ASC);
	END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION trolls(moment BIGINT) RETURNS TABLE(returned_member INT, votes_for INT, votes_against INT, is_active BOOLEAN) AS $$
BEGIN
	RETURN QUERY (SELECT members.id, members.votes_for, members.votes_against, is_active(moment, members.id) FROM members WHERE members.votes_for < members.votes_against ORDER BY (members.votes_for - members.votes_against), members.id ASC);
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
IF 'app' NOT IN (SELECT rolname FROM pg_catalog.pg_roles) THEN
	CREATE USER app WITH ENCRYPTED PASSWORD 'qwerty';
END IF;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app;
GRANT UPDATE ON ALL TABLES IN SCHEMA public TO app;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO app;
GRANT INSERT ON ALL TABLES IN SCHEMA public TO app;
END
$$;

COMMIT;