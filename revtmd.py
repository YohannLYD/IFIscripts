import sys
import subprocess
import os
import time
import pdb
from easygui import multenterbox, choicebox, multchoicebox

if len(sys.argv) < 2:
    print '\nUSAGE: PYTHON REVTMD.PY FILENAME\n'
    print 'Requires EASYGUI\n'    
    sys.exit()
else:
    # Store the filename for the XML sidecar.
    revtmd_xmlfile = sys.argv[1] + '.xml'
    mediaxml = sys.argv[1] + '_mediainfo.xml'

    # Store the filename without extension.
    filename_without_path = os.path.basename(sys.argv[1])

    # Store the current time in ISO8601 format.
    time_date = time.strftime("%Y-%m-%dT%H:%M:%S")
    date = time.strftime("%Y-%m-%d")
    def get_audio_stream_count():
        audio_stream_count = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'flat', sys.argv[1]]).splitlines()
        return len(audio_stream_count)
    audio_tracks = get_audio_stream_count()
    if audio_tracks > 0:
        sound = "Yes"
    elif audio_tracks == 0:
        sound = "No"

        
    # Begin creating functions for repetitive tasks:
    # Generate xml elements for coding process history.
    def revtmd_coding_process_history():
        fo.write('<revtmd:codingProcessHistory>\n')
        fo.write('<revtmd:role/>\n')
        fo.write('<revtmd:description/>\n')
        fo.write('<revtmd:manufacturer/>\n')
        fo.write('<revtmd:modelName/>\n')
        fo.write('<revtmd:version/>\n')
        fo.write('<revtmd:serialNumber/>\n')
        fo.write('<revtmd:signal/>\n')
        fo.write('<revtmd:settings/>\n')
        fo.write('<revtmd:settings/>\n')
        fo.write('<revtmd:settings/>\n')
        fo.write('<revtmd:settings/>\n')
        fo.write('<revtmd:settings/>\n')
        fo.write('<revtmd:settings/>\n')
        fo.write('<revtmd:videoEncoding/>\n')
        fo.write('</revtmd:codingProcessHistory>\n')
    #pdb.set_trace()
    def get_xml_output(xpath, element, source_xml,xml_variable):
        command =  ['xml','sel', '-t', '-m', xpath, '-v', element, source_xml ]
        xml_variable = subprocess.Popen(command, stdout=subprocess.PIPE)
        xml_variable = xml_variable.communicate()[0]
        
        return xml_variable
    
    def revtmd_blank_audio_fields():
        
        
        global audio_track_number		
        audio_track_number = 1
        while audio_track_number <= audio_tracks:
            if audio_tracks == 1:
                typeoo = "Mediainfo/File/track[@type='Audio']"
            else:
                typeoo = "Mediainfo/File/track[@type='Audio' and @typeorder=%s]" % (audio_track_number)
            #acodec = subprocess.check_output(['xml','sel', '-t', '-m', typeoo, '-v', 'Codec', mediaxml ])    
            #aendian = subprocess.check_output(['xml','sel', '-t', '-m', typeoo, '-v', 'Codec_Settings_Endianness', mediaxml ])    
            #command =  ['xml','sel', '-t', '-m', typeoo, '-v', 'Codec_Settings_Endianness', mediaxml ]
            #aendian = subprocess.Popen(command, stdout=subprocess.PIPE)
            #aendian = aendian.communicate()[0]
            aendian = get_xml_output(typeoo,'Codec_SettingsEndianness', mediaxml, 'aendian')
            abitdepth = get_xml_output(typeoo,'Resolution', mediaxml, 'abitdepth')
            acodec = get_xml_output(typeoo,'Codec', mediaxml, 'acodec')
            channel_count = get_xml_output(typeoo,'Channel_s_', mediaxml, 'channel_count')        
            asize = get_xml_output(typeoo,'StreamSize', mediaxml, 'asize')
            compression_mode = get_xml_output(typeoo,'Compression_Mode', mediaxml, 'compression_mode')
            sample_rate = get_xml_output(typeoo,'SamplingRate', mediaxml, 'sample_rate')
            
            
            #abitdepth = subprocess.check_output(['xml','sel', '-t', '-m', typeoo, '-v', 'Resolution', mediaxml ])    
            #asize = subprocess.check_output(['xml','sel', '-t', '-m', typeoo, '-v', 'StreamSize', mediaxml ])    

            fo.write('<revtmd:track id="%s" type="audio">\n' % audio_track_number)
            fo.write('<revtmd:duration/>\n')
            fo.write('<revtmd:size>%s</revtmd:size>\n' % asize)
            fo.write('<revtmd:codec>\n')
            fo.write('<revtmd:codecID>%s</revtmd:codecID>\n' % acodec)
            fo.write('<revtmd:channelCount>%s</revtmd:channelCount>\n' % channel_count)
            fo.write('<revtmd:endianness>%s</revtmd:endianness>\n' % aendian)
            fo.write('<revtmd:quality>%s</revtmd:quality>\n'% compression_mode)
            fo.write('</revtmd:codec>\n')
            fo.write('<revtmd:bitsPerSample>%s</revtmd:bitsPerSample>\n'% abitdepth)
            fo.write('<revtmd:samplingRate>%s</revtmd:samplingRate>\n' % sample_rate)
             
            fo.write('<revtmd:bitsPerSample/>\n')
            fo.write('<revtmd:sampling/>\n')
            fo.write('</revtmd:track>\n')
                
            audio_track_number += 1
            #PS C:\Users\kieranjol> xml sel -t -m "Mediainfo/File/track[@type='Audio' and @typeorder='12']" -v ID D:\mi.xml
            
        
    with open(mediaxml, "w+") as fo:
            mediaxmlinput = subprocess.check_output(['mediainfo',
                                '-f',
                                '--language=raw', # Use verbose output.
                                '--output=XML',
                                sys.argv[1] ])       #input filename
            fo.write(mediaxmlinput)
        

    # This function actually adds value to a specified xml element.    
    def add_to_revtmd(element, value, xmlfile):
        subprocess.call(['xml', 'ed', '--inplace', '-N', 'x=http://nwtssite.nwts.nara/schema/', '-u', element, '-v', value, xmlfile])

        # What follows are a lot of functions that can be reused. Titles should be self explanatory.

    def get_mediainfo(var_type, type, filename):
        var_type = subprocess.check_output(['mediainfo', '--Language=raw', '--Full',
                                             type , filename ]).replace('\n', '').replace('\r', '')
        return var_type
    # Begin Interview using Easygui.
    msg ="Which Workflow?"
    title = "Workflows"
    choices = ["Telecine One Light", "bestlight", "Telecine Grade", "Tape Ingest 1", "Tape Ingest 2", "Tape Edit Suite 1", "Tape Edit Suite 2"]
    workflow = choicebox(msg, title, choices)

    # Forking path in order to get more accurate info depending on workflow
    if workflow not in ("Telecine One Light", "bestlight", "Telecine Grade"):
        no_of_emptyfields = 13 #temp, this will be a variable.
        msg ="Tape Deck?"
        title = "Pick a name yo!"
        choices = ["DVW-500P", "MiniDV-Something", "UVW-1400AP", "DVW-510P", "J-30", "J-H3", "UVW-1200P", "Unknown"]
        deck = choicebox(msg, title, choices)
        print deck
        if deck == "DVW-A500P":
            def deck_func(numbo):
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Playback', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Sony', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'DVW-A500P', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'SDI', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', '10317', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:settings[1]', 'Timecode = Auto', revtmd_xmlfile)  
        if deck == "DVW-510P":
            def deck_func(numbo):
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Playback', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Sony', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'DVW-A510p', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'SDI', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', '11414', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:settings[1]', 'Timecode = Auto', revtmd_xmlfile)   
        elif deck == "J-30":
            def deck_func(numbo):
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Playback', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Sony', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'J-30', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'SDI', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', 'ABC123', revtmd_xmlfile)
        elif deck == "J-H3":
            def deck_func(numbo):
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Playback', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Sony', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'J-H3', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'SDI', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', '11482', revtmd_xmlfile)    
        elif deck == "UVW-1400AP":
            def deck_func(numbo):
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Playback', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Sony', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'UVW-1400AP', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'Component', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', '13697', revtmd_xmlfile) 
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:settings[1]', 'Component out = Y-R,B', revtmd_xmlfile)   
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:settings[2]', 'Timecode = LTC', revtmd_xmlfile)    
                  
        elif deck == "UVW-1200P":
            def deck_func(numbo):
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Playback', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Sony', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'UVW-1200P', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'Component', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', '13697', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:settings[1]', 'Component out = Y-R,B', revtmd_xmlfile)   
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:settings[2]', 'Timecode = LTC', revtmd_xmlfile)                  
    if workflow == "Tape Ingest 1":
        def workstation(numbo):
            add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Host Computer', revtmd_xmlfile)
            add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Hewlett Packard', revtmd_xmlfile)
            add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'ABC123', revtmd_xmlfile)
            add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:version', 'ABC123', revtmd_xmlfile)
            add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', 'ABC123', revtmd_xmlfile)
        no_of_emptyfields = 6
    elif workflow == "Tape Ingest 2":
        def workstation(numbo):
            add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Host Computer', revtmd_xmlfile)
            add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Hewlett Packard2', revtmd_xmlfile)
            add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'ABC123', revtmd_xmlfile)
            add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:version', 'ABC123', revtmd_xmlfile)
            add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', 'ABC123', revtmd_xmlfile)
    # Currently unused, but I'll get around to it :[
    else:
        no_of_emptyfields = 13
        if workflow == "Telecine Grade":
            msg = "Interventions post capture"
            title = "Interventions post capture?"
            fieldNames = ["Colour Alterations","Exposure Alterations","Sound Alterations"]
            grade_interventions = []  # we start with blanks for the values
            grade_interventions = multenterbox(msg,title, fieldNames)
        
        else:
            
            msg = "Capture Frame Rate"
            title = "Capture Frame Rate"
            fieldNames = ["15","16","18","20","22","25"]
            capture_frame_rate = []  # we start with blanks for the values
            capture_frame_rate = choicebox(msg,title, fieldNames)
            fps_string = 'Captured at %s fps' % capture_frame_rate
            
            msg ="Telecine Machine"
            title = "Choose the telecine machine"
            choices = ["Flashtransfer", "Flashscan",]
            scanner = choicebox(msg, title, choices)
        
        if scanner == "Flashtransfer":
            def scanner(numbo):            
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Telecine', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', '16mm Film Digitisation', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'MWA', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'Flashtransfer', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'SDI', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', 'ABC123', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:settings', fps_string, revtmd_xmlfile)
        if scanner == "Flashscan":
            def scanner(numbo):            
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Telecine', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', '8mm Film Digitisation', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'MWA', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'Flashscan', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'SDI', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', 'ABC123', revtmd_xmlfile)
                add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:settings[1]', fps_string, revtmd_xmlfile)
                
                
      
        
        
        msg ="Preperation?"
        title = "Workflows"
        choices = ["Splice and perforation check on rewind table",
                   "Splice repairs",
                   "Leader added", 
                   "Perforation repairs",
                   "Recanned",
                   "Film reversed during transfer"    ]
        preparation = multchoicebox(msg, title, choices)
        print preparation
        
        msg ="Interventions at point of capture"
        title = "capture interventions"
        choices = ["Exposure compensation",
                   "Contrast adjustment",
                   "Positive to negative", 
                   "Spacing between reels not captured",
                    ]
        capture_interventions = multchoicebox(msg, title, choices)
        print capture_interventions
        
        msg ="Post Processing?"
        title = "Post Processing"
        choices = ["Horizontal Flipping",
                   "Vertical Flipping",
                   "Audio normalised to -20db", 
                   "Broadcast Safe Filter",
                   "Desaturate Filter",
                   "Positive to Negative",
                   "Avid Motion Editing"
                   ]
        post_processing = multchoicebox(msg, title, choices)
        print post_processing
    '''
    if preparation == "Splice and perforation check & repairs":
        def prep():
            add_to_revtmd('//revtmd:preparationActions[1]', 'Check for splices and perforation damage', revtmd_xmlfile)
            add_to_revtmd('//revtmd:preparationActions[2]', 'Carry out repairs', revtmd_xmlfile)
     '''


    #More interviews    
    msg ="User?"
    title = "Pick a name yo!"
    choices = ["Kieran O'Leary", "Gavin Martin", 
               "Dean Kavanagh", "Raelene Casey", 
           "Anja Mahler", "Eoin O'Donohoe", "Unknown"]
    user = choicebox(msg, title, choices)


    msg = "Fill out these things please"
    title = "blablablabl"
    fieldNames = ["Source Accession Number",
                  "Notes","Filmographic Reference Number", 
                  "Identifier-Object Entry/Accession Number:"]
      # we start with blanks for the values
    fieldValues = multenterbox(msg,title, fieldNames)
    print fieldValues

    # make sure that none of the fields was left blank
    while 1:
            if fieldValues == None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" is a required field.' % fieldNames[i])
            if errmsg == "": break # no problems found
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
    print fieldValues  
    # Prints info to screen. Make this actually useful! 
    #print "Reply was:", fieldValues
    #print "Your selection was:\n Workflow =  %s\n Scanner = %s\n Preparation actions = %s\n User = %s\n" % (workflow,scanner, preparation, user)

    # Generate filename for the reVTMD xmlfile
    revtmd_xmlfile = sys.argv[1] + '.xml'


    # Store md5 checksum.
    print 'generating md5 checksum, this may take some time'
    md5 = subprocess.check_output(['md5deep', '-e', sys.argv[1]])
    
    duration =  get_mediainfo('duration', '--inform=Video;%Duration_String4%', sys.argv[1] )
    par =  get_mediainfo('par', '--inform=Video;%PixelAspectRatio%', sys.argv[1] )
    dar =  get_mediainfo('dar', '--inform=Video;%DisplayAspectRatio%', sys.argv[1] )
    width =  get_mediainfo('width', '--inform=Video;%Width%', sys.argv[1] )
    height =  get_mediainfo('height', '--inform=Video;%Height%', sys.argv[1] )
    vcodec =  get_mediainfo('dar', '--inform=Video;%Codec%', sys.argv[1] )
    size =  get_mediainfo('size', '--inform=Video;%StreamSize%', sys.argv[1] )
    chromasubsampling =  get_mediainfo('chromasubsampling', '--inform=Video;%ChromaSubsampling%', sys.argv[1] )
    codec_id =  get_mediainfo('codecid', '--inform=Video;%CodecID%', sys.argv[1] )
    scantype =  get_mediainfo('scantype', '--inform=Video;%ScanType%', sys.argv[1] )
    scanorder =  get_mediainfo('scanorder', '--inform=Video;%ScanOrder%', sys.argv[1] )
    bitspersample =  get_mediainfo('bitspersample', '--inform=Video;%BitDepth%', sys.argv[1] )
    quality =  get_mediainfo('quality', '--inform=Video;%Compression_Mode%', sys.argv[1] )
    container_duration =  get_mediainfo('container_duration', '--inform=General;%Duration_String4%', sys.argv[1] )
    container_size =  get_mediainfo('container_size', '--inform=General;%FileSize%', sys.argv[1] )
    overall_bitrate =  get_mediainfo('overall_bitrate', '--inform=General;%OverallBitRate%', sys.argv[1] )
    video_bitrate =  get_mediainfo('video_bitrate', '--inform=Video;%BitRate%', sys.argv[1] )
    container_mime =  get_mediainfo('container_mime', '--inform=General;%InternetMediaType%', sys.argv[1] )
    frame_rate =  get_mediainfo('frame_rate', '--inform=Video;%FrameRate%', sys.argv[1] )
    container_frame_rate =  get_mediainfo('container_frame_rate', '--inform=General;%FrameRate%', sys.argv[1] )
    frame_count =  get_mediainfo('frame_count', '--inform=Video;%FrameCount%', sys.argv[1] )


    # Create mostly blank reVTMD template which we'll gradually fill up with info.
    with open(revtmd_xmlfile, "w+") as fo:

        fo.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fo.write('<revtmd xmlns:revtmd="http://nwtssite.nwts.nara/schema/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://nwtssite.nwts.nara/schema/  http://www.archives.gov/preservation/products/reVTMD.xsd">\n')
        fo.write('<revtmd:reVTMD>\n')
        fo.write('<revtmd:object>\n')
        fo.write('<revtmd:filename/>\n')
        fo.write('<revtmd:organization>\n')
        fo.write('<revtmd:organization_main>\n')
        fo.write('<revtmd:name>Irish Film Institute</revtmd:name>\n')
        fo.write('<revtmd:role/>\n')
        fo.write('</revtmd:organization_main>\n')
        fo.write('<revtmd:organization_division>\n')
        fo.write('<revtmd:name>Irish Film Archive</revtmd:name>\n')
        fo.write('</revtmd:organization_division>\n')
        fo.write('</revtmd:organization>\n')
        fo.write('<revtmd:identifier type="Object Entry">%s</revtmd:identifier>\n' % fieldValues[3])
        fo.write('<revtmd:identifier type="Inmagic DB Textworks Filmographic Reference Number">%s</revtmd:identifier>\n' % fieldValues[2])
        fo.write('<revtmd:mimetype>%s</revtmd:mimetype>\n' % container_mime)
        fo.write('<revtmd:duration>%s</revtmd:duration>\n' % container_duration)
        fo.write('<revtmd:language/>\n')
        fo.write('<revtmd:size>%s</revtmd:size>\n' % container_size)
        fo.write('<revtmd:datarate>%s</revtmd:datarate>\n' % overall_bitrate)
        fo.write('<revtmd:use>Preservation Master</revtmd:use>\n')
        fo.write('<revtmd:color/>\n')
        fo.write('<revtmd:framerate>%s</revtmd:framerate>\n' % container_frame_rate)
        fo.write('<revtmd:format/>\n')
        fo.write('<!-- Checksum as generated immediately after the digitization process. -->\n')
        fo.write('<revtmd:checksum algorithm="md5" dateTime="%s">%s</revtmd:checksum>\n' % (time_date,md5.split()[0])) 
        
        fo.write('<revtmd:sound>%s</revtmd:sound>\n' % sound)
        fo.write('<revtmd:track id="1" type="video">\n')
        fo.write('<revtmd:duration/> \n')
        fo.write('<revtmd:size/>\n')
        fo.write('<revtmd:dataRate/>\n' )
        fo.write('<revtmd:color/>\n')
        fo.write('<revtmd:frame>\n')
        fo.write('<revtmd:pixelsHorizontal/>\n')
        fo.write('<revtmd:pixelsVertical/>\n')
        fo.write('<revtmd:PAR/>\n')
        fo.write('<revtmd:DAR/>\n')
        fo.write('</revtmd:frame>\n')
        fo.write('<revtmd:frameRate>%s</revtmd:frameRate>\n' % frame_rate)
        fo.write('<revtmd:codec>\n')
        fo.write('<revtmd:codecID/>\n')
        fo.write('<revtmd:channelCount/>\n')
        fo.write('<revtmd:endianness/>\n')
        fo.write('<revtmd:quality/>\n')
        fo.write('<revtmd:scanType/>\n')
        fo.write('<revtmd:scanOrder/>\n')
        
        fo.write('</revtmd:codec>\n')
        fo.write('<revtmd:bitsPerSample/>\n')
        fo.write('<revtmd:sampling/>\n')
        fo.write('<revtmd:frameCount>%s</revtmd:frameCount> \n' % frame_count)
        
        fo.write('</revtmd:track>\n')
        revtmd_blank_audio_fields()
        fo.write('<revtmd:captureHistory>\n')
        fo.write('<revtmd:digitizationDate>%s</revtmd:digitizationDate>\n' % date)
        fo.write('<revtmd:digitizationEngineer/>\n')
        fo.write('<revtmd:preparationActions/>\n')
        fo.write('<revtmd:preparationActions/>\n')
        fo.write('<revtmd:preparationActions/>\n')
        fo.write('<revtmd:preparationActions/>\n')
        fo.write('<revtmd:preparationActions/>\n')
        fo.write('<revtmd:preparationActions/>\n')
        fo.write('<revtmd:source/>\n')
        for _ in range(no_of_emptyfields):    
            revtmd_coding_process_history()
        fo.write('</revtmd:captureHistory>\n')
        fo.write('</revtmd:object>\n')
        fo.write('</revtmd:reVTMD>\n')
        fo.write('</revtmd>\n')





    
    

    numbo1 = 1
    if preparation != None:

        for prep_actions in preparation: 
                 add_to_revtmd('//revtmd:preparationActions' + '[' + str(numbo1) + ']' , prep_actions, revtmd_xmlfile)
                 numbo1 += 1    

     
    def tech_metadata_revtmd():
        add_to_revtmd('//revtmd:duration', duration, revtmd_xmlfile)
        add_to_revtmd('//revtmd:PAR', par, revtmd_xmlfile)
        add_to_revtmd('//revtmd:DAR', dar, revtmd_xmlfile)
        add_to_revtmd('//revtmd:pixelsHorizontal', width, revtmd_xmlfile)
        add_to_revtmd('//revtmd:pixelsVertical', height, revtmd_xmlfile)
        add_to_revtmd('//revtmd:track[@id="1" and @type="video"]/revtmd:size', size, revtmd_xmlfile)
        add_to_revtmd('//revtmd:track[@id="1" and @type="video"]/revtmd:sampling', chromasubsampling, revtmd_xmlfile)
        add_to_revtmd('//revtmd:track[@id="1" and @type="video"]//revtmd:codecID', codec_id, revtmd_xmlfile)
        add_to_revtmd('//revtmd:track[@id="1" and @type="video"]//revtmd:scanType', scantype, revtmd_xmlfile)
        add_to_revtmd('//revtmd:track[@id="1" and @type="video"]/revtmd:bitsPerSample', bitspersample, revtmd_xmlfile)
        add_to_revtmd('//revtmd:track[@id="1" and @type="video"]//revtmd:quality', quality, revtmd_xmlfile)
        add_to_revtmd('//revtmd:track[@id="1" and @type="video"]//revtmd:scanOrder', scanorder, revtmd_xmlfile)
        add_to_revtmd('//revtmd:track[@id="1" and @type="video"]//revtmd:duration', duration, revtmd_xmlfile)
        add_to_revtmd('//revtmd:track[@id="1" and @type="video"]//revtmd:dataRate', video_bitrate , revtmd_xmlfile)
        
        


    def ffmpeg_revtmd(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Transcode', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', 'Transcode to FFv1 in Matroska wrapper', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'ffmpeg', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', '2.8.2', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:videoEncoding', "FFv1", revtmd_xmlfile)

    def avid_capture_revtmd(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Capture Software', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', 'SDI bitstream capture', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Avid', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'Media Composer', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:version', '8.3.0', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', 'ABC123', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:videoEncoding', "Avid 1:1 10-bit", revtmd_xmlfile) #bot sure of 4cc right now, maybe AVup?
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:audioEncoding', "PCM", revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:videoBitDepth', "10", revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:audioBitDepth', "abc123", revtmd_xmlfile)
    def control_room_capture_revtmd(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Capture Software', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'AJA', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'Control Room', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:version', 'ABC123', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', 'ABC123', revtmd_xmlfile)   
    def telecine_mac_pro_revtmd(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Host Computer', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', 'Provides computing environment', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Apple', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'Mac Pro', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:version', 'dunno', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', 'ABC123', revtmd_xmlfile)


    def telecine_mac_pro_os_revtmd(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Host Computer Operating System', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', 'Provides computing environment operating system', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Apple', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'Mavericks', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:version', 'dunno', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', 'ABC123', revtmd_xmlfile)
    def win7_hp_revtmd(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Host Computer Operating System', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Windows', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', '7 Professional', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:version', 'Service pack X', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', 'ABC123', revtmd_xmlfile)
    def avid_export_revtmd(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Transcode', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', 'Transcode to v210 in quicktime wrapper', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Avid', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'Media Composer', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:version', '8.3.0', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:videoEncoding', "v210", revtmd_xmlfile)
    def bmd_us4k_revtmd(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Capture Card', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', 'Capture SDI signal', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Blackmagic', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'Ultrastudio 4k', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:version', '10.5', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', "SDI", revtmd_xmlfile)
    def bmd_miniconverter_revtmd(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Analog to digital converter', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Blackmagic', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'Mini-Converter Analog to SDI', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', '334080', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', "SDI", revtmd_xmlfile)
    def avid_consolidate_revtmd(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'File Editing', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', 'Add plate, consolidate multiple clips', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Avid', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'Media Composer', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:version', '8.3.0', revtmd_xmlfile)
    def avid_post_processing(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Post Processing', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Avid', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'Media Composer', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:version', '8.3.0', revtmd_xmlfile)
        
        
    '''
    to do - add in bmd a2d, and add aja kona as a capture card.
    '''
    def aja_analog2digital(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Analog to Digital Converter', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', '', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'AJA', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'KONA LHe Plus', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'SDI', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', 'ABC123', revtmd_xmlfile)
    def aja_kona_capture_ingest1(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Capture Card', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', 'Capture SDI Signal', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'AJA', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'KONA LHe Plus', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'SDI', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', '00T59106', revtmd_xmlfile)
    def aja_kona_capture_ingest2(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Capture Card', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', 'Capture SDI Signal', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'AJA', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'KONA LHe Plus', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'SDI', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', '00T59109', revtmd_xmlfile)
    def IiyamaMonitor_ingest1(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Host Computer Monitor', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', '', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Iiyama', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'ProLite B2480HS/B1', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'DVI', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', '11183M4504454', revtmd_xmlfile)
    def IiyamaMonitor_ingest2(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Host Computer Monitor', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', '', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Iiyama', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'ProLite B2480HS/B1', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'DVI', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', '11183M4504437', revtmd_xmlfile)
    def IiyamaMonitor_telecine(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Host Computer Monitor', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', '', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Iiyama', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'ProLite B2480HS/B1', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'DVI', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', 'TBD', revtmd_xmlfile)
    def bmd_ultrascopes_ingest1(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Quality Assesment', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', 'Digital Scopes', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Blackmagic Design', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'Smartscope Duo 4K', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'SDI', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', '1969088', revtmd_xmlfile)        
    def bmd_ultrascopes_ingest2(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Quality Assesment', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', 'Digital Scopes', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Blackmagic Design', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'Smartscope Duo 4K', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'SDI', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', '1968794', revtmd_xmlfile)        
    def bmd_ultrascopes_telecine(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Quality Assesment', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', 'Digital Scopes', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'Blackmagic Design', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'Smartscope Duo 4K', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'SDI', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', 'TBD', revtmd_xmlfile)        
    def tvlogic_broadcast_ingest1(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Quality Assesment', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', 'Ingest 1 Broadcast Monitor', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'TV Logic', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'LVM-245W', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'SDI', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', 'LV245N0047', revtmd_xmlfile)        
    def tvlogic_broadcast_ingest2(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Quality Assesment', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', 'Ingest 2 Broadcast Monitor', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'TV Logic', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'LVM-245W', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'SDI', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', 'LV245N0157', revtmd_xmlfile)    
    def tvlogic_broadcast_telecine(numbo):
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:role', 'Quality Assesment', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:description', 'Telecine Broadcast Monitor', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:manufacturer', 'TV Logic', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:modelName', 'LVM-245W', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:signal', 'SDI', revtmd_xmlfile)
        add_to_revtmd('//revtmd:codingProcessHistory' + str([numbo]) + '/revtmd:serialNumber', 'TBD', revtmd_xmlfile)    

    # Combine previous functions for the bestlight workflow  
    def bestlight():
        add_to_revtmd('//revtmd:filename', filename_without_path, revtmd_xmlfile)
        add_to_revtmd('//revtmd:source', fieldValues[0], revtmd_xmlfile)
        scanner(2)
        IiyamaMonitor_telecine(5)
        tvlogic_broadcast_telecine(6)
        bmd_ultrascopes_telecine(7)
        tech_metadata_revtmd()
        bmd_us4k_revtmd(1)
        avid_capture_revtmd(8)
        add_to_revtmd('//revtmd:digitizationEngineer[1]', user, revtmd_xmlfile)
        avid_consolidate_revtmd(9)
        avid_export_revtmd(10)
        #ffmpeg_revtmd(8)
        telecine_mac_pro_revtmd(3)
        telecine_mac_pro_os_revtmd(4)
        avid_post_processing(11)
        print post_processing
        if post_processing != None:
            numbo2 = 1
            for post in post_processing:
             
             
                add_to_revtmd('//revtmd:codingProcessHistory[11]' + '/revtmd:settings' + '[' + str(numbo2) + ']' , post, revtmd_xmlfile)
                numbo2 += 1
                
        if capture_interventions != None:
            numbo2 = 2
            for interventions in capture_interventions:
             
             
                add_to_revtmd('//revtmd:codingProcessHistory[2]' + '/revtmd:settings' + '[' + str(numbo2) + ']' , interventions, revtmd_xmlfile)
                numbo2 += 1    
        else:
            print 'all is well'
        

    def ingest1():
        add_to_revtmd('//revtmd:filename', filename_without_path, revtmd_xmlfile)
        add_to_revtmd('//revtmd:source', fieldValues[0], revtmd_xmlfile)
        add_to_revtmd('//revtmd:digitizationEngineer[1]', user, revtmd_xmlfile)
        aja_analog2digital(4)
        tech_metadata_revtmd()
        win7_hp_revtmd(3)
        #ffmpeg_revtmd(6)
        workstation(2)
        control_room_capture_revtmd(5)
        deck_func(1)
    def ingest2():
        add_to_revtmd('//revtmd:filename', filename_without_path, revtmd_xmlfile)
        add_to_revtmd('//revtmd:source', fieldValues[0], revtmd_xmlfile)
        add_to_revtmd('//revtmd:digitizationEngineer[1]', user, revtmd_xmlfile)
        aja_analog2digital(4)
        tech_metadata_revtmd()
        win7_hp_revtmd(3)
        ffmpeg_revtmd(6)
        workstation(2)
        control_room_capture_revtmd(5)
        deck_func(1)

    # This launches the xml creation based on your selections  
    if workflow == "bestlight":
        bestlight()
    elif workflow =="Tape Ingest 1":
        if deck not in ("UVW-1400AP", "UVW-1200P"):
            ingest1()
        else:
            def betasp_ingest1():
                add_to_revtmd('//revtmd:filename', filename_without_path, revtmd_xmlfile)
                add_to_revtmd('//revtmd:source', fieldValues[0], revtmd_xmlfile)
                add_to_revtmd('//revtmd:digitizationEngineer[1]', user, revtmd_xmlfile)
                aja_kona_capture_ingest1(5)
                tech_metadata_revtmd()
                win7_hp_revtmd(3)
                
                workstation(2)
                control_room_capture_revtmd(6)
                deck_func(1)
                bmd_miniconverter_revtmd(4)
            betasp_ingest1()
            
    elif workflow =="Tape Ingest 2":
        ingest2()

    # Temporary, possibly permanent way to delete empty elements
    subprocess.call(['xml', 'ed', '--inplace','-d',
                    '//*[not(./*) and (not(./text()) or normalize-space(./text())="")]',
                     revtmd_xmlfile])