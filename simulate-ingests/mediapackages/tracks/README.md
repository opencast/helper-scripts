# Mediapackage Tracks Directory
Video and audio tracks should be present here that match the tracks listed in the mediapackage 
profiles. The filenames must have the form:

    [presenation|presenter]-<type>-<duration>.[avi|mp3]

e.g

    presenter-single-1.avi
    
## Filtering Sample Mediapackage from Database

Analysing the mediapackage xml in the archive is expensive, therefore create a temporary table (#tablename) for 
selecting prospective tracks:

    /* create temp table */
    with xmlnamespaces (default 'http://mediapackage.opencastproject.org')
    select
      id,
      mp.value('(/mediapackage/media/track/@type)[1]', 'varchar(256)') as track_1,
      left(mp.value('(/mediapackage/media/track/mimetype)[1]', 'varchar(256)'), 5) as mime_1,
      mp.value('(/mediapackage/media/track/@type)[2]', 'varchar(256)') as track_2,
      left(mp.value('(/mediapackage/media/track/mimetype)[2]', 'varchar(256)'), 5) as mime_2,
      mp.value('(/mediapackage/media/track/@type)[3]', 'varchar(256)') as track_3,
      left(mp.value('(/mediapackage/media/track/mimetype)[3]', 'varchar(256)'), 5) as mime_3,
      mp.value('(/mediapackage/@duration)[1]', 'int')/60000 as duration
      into #mp_data
      from
      /* Cast the xml strings to UTF-16 encoded xml fields */
      (select id, cast(replace(cast(mediapackage_xml as nvarchar(max)), 'UTF-8', 'UTF-16') as xml) as mp
        from dbo.mh_archive_episode
        /* Pre filter the data */
        where modification_date > '2017-01-10 00:00:00'
        and version = 0 and deleted = 0) as mpxml;
        
Once the temporary table #mp_data has been created queries can be run against it get ids of prospective example 
mediapackages:

    select id
      from #mp_data
      where
        duration=55
        and track_1='presenter/source' and mime_1='video'
        and track_2='presenter/source' and mime_2='audio'
        and track_3 is null and mime_3 is null;

