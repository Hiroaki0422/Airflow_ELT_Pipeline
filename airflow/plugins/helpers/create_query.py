class CreateQueries:
	staging_events_table_create= ("""
	    CREATE TABLE staging_events
	    (
	        artist varchar,
	        auth varchar(20),
	        firstName varchar,
	        gender varchar(1),
	        itemInSession smallint,
	        lastName varchar,
	        length numeric,
	        level varchar(10),
	        location varchar,
	        method varchar(5),
	        page varchar,
	        registration numeric,
	        sessionId smallint,
	        song varchar, 
	        status smallint,
	        ts bigint,
	        userAgent varchar(200),
	        userID smallint
	    );
    
""")

	staging_songs_table_create = ("""
	    CREATE TABLE staging_songs
	    (
	        num_songs smallint,
	        artist_id varchar(20),
	        artist_latitude numeric,
	        artist_longitude numeric,
	        artist_location varchar,
	        artist_name varchar,
	        song_id varchar(20),
	        title varchar,
	        duration numeric,
	        year smallint
	    );
""")

	songplay_table_create = ("""
	    CREATE TABLE songplay
	    (
	        songplay_id int IDENTITY(0,1), 
	        start_time timestamp NOT NULL, 
	        user_id smallint, 
	        level varchar(5), 
	        song_id varchar(20), 
	        artist_id varchar(20), 
	        session_id smallint, 
	        location varchar(100), 
	        user_agent varchar(200),
	        PRIMARY KEY(songplay_id) 
	    );
""")

	user_table_create = ("""
	    CREATE TABLE users
	    (
	        user_id smallint, 
	        first_name varchar(40), 
	        last_name varchar(40), 
	        gender varchar(1), 
	        level varchar(5)
	    );
	""")

	song_table_create = ("""
	    CREATE TABLE songs
	    (
	        song_id varchar(20) NOT NULL, 
	        title varchar, 
	        artist_id varchar(20), 
	        year smallint, 
	        duration numeric
	    );
	""")

	artist_table_create = ("""
	    CREATE TABLE artists
	    (
	        artist_id varchar(20) NOT NULL, 
	        name varchar, 
	        location varchar, 
	        latitude float, 
	        longitude float
	    );
	""")

	time_table_create = ("""
	    CREATE TABLE time (
	        start_time timestamp NOT NULL, 
	        hour smallint NOT NULL, 
	        day smallint NOT NULL, 
	        week smallint NOT NULL, 
	        month smallint NOT NULL, 
	        year smallint NOT NULL, 
	        weekday smallint NOT NULL
	    );
	""")

	all_tables_create = ("""
		DROP TABLE IF EXISTS staging_events;
		DROP TABLE IF EXISTS staging_songs;
		DROP TABLE IF EXISTS songplays;
		DROP TABLE IF EXISTS users;
		DROP TABLE IF EXISTS songs;
		DROP TABLE IF EXISTS artists;
		DROP TABLE IF EXISTS time;

		CREATE TABLE public.artists (
			artistid varchar(256) NOT NULL,
			name varchar(256),
			location varchar(256),
			lattitude numeric(18,0),
			longitude numeric(18,0)
		);

		CREATE TABLE public.songplays (
			playid varchar(32) NOT NULL,
			start_time timestamp NOT NULL,
			userid int4 NOT NULL,
			"level" varchar(256),
			songid varchar(256),
			artistid varchar(256),
			sessionid int4,
			location varchar(256),
			user_agent varchar(256),
			CONSTRAINT songplays_pkey PRIMARY KEY (playid)
		);

		CREATE TABLE public.songs (
			songid varchar(256) NOT NULL,
			title varchar(256),
			artistid varchar(256),
			"year" int4,
			duration numeric(18,0),
			CONSTRAINT songs_pkey PRIMARY KEY (songid)
		);

		CREATE TABLE public.staging_events (
			artist varchar(256),
			auth varchar(256),
			firstname varchar(256),
			gender varchar(256),
			iteminsession int4,
			lastname varchar(256),
			length numeric(18,0),
			"level" varchar(256),
			location varchar(256),
			"method" varchar(256),
			page varchar(256),
			registration numeric(18,0),
			sessionid int4,
			song varchar(256),
			status int4,
			ts int8,
			useragent varchar(256),
			userid int4
		);

		CREATE TABLE public.staging_songs (
			num_songs int4,
			artist_id varchar(256),
			artist_name varchar(256),
			artist_latitude numeric(18,0),
			artist_longitude numeric(18,0),
			artist_location varchar(256),
			song_id varchar(256),
			title varchar(256),
			duration numeric(18,0),
			"year" int4
		);

		CREATE TABLE public."time" (
			start_time timestamp NOT NULL,
			"hour" int4,
			"day" int4,
			week int4,
			"month" varchar(256),
			"year" int4,
			weekday varchar(256),
			CONSTRAINT time_pkey PRIMARY KEY (start_time)
		);

		CREATE TABLE public.users (
			userid int4 NOT NULL,
			first_name varchar(256),
			last_name varchar(256),
			gender varchar(256),
			"level" varchar(256),
			CONSTRAINT users_pkey PRIMARY KEY (userid)
		);
		""")
