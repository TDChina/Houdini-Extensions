# Default script run when a camera object is created
# $arg1 is the name of the object to create

\set noalias = 1
if ( "$arg1" != "" ) then
    opparm $arg1 use_dcolor( 0 )
    opproperty -f $arg1 mantra default_camera
    opparm $arg1 resx 1920 resy 1080
    opcf $arg1
    # Add default geometry
    opadd -n file file1
    opparm file1 file defcam.bgeo
    oplocate -x 0.18 -y 3.0 file1
    opset -d off -r off -t off -l off -s off -u off file1
    opadd -n add camOrigin
    oplocate -x 2.0 -y 3.0 camOrigin
    opparm camOrigin points ( 1 ) usept0 ( 1 ) pt0 ( 0 0 0 )
    opset -d off -r off -t off -l off -s off -u off camOrigin
    opadd -n xform xform1
    oplocate -x 0.18 -y 1.5 xform1
    chblockbegin
    chadd -t 0 0 xform1 scale
    chkey -t 0 -T a -F 'property("../iconscale", 1)' xform1/scale
    chblockend
    opparm xform1 scale ( scale )
    chlock xform1 -*
    opset -d on -r on -t off -l off -s off -u off xform1
    oporder -e file1 xform1
    opwire file1 -0 xform1
    opcf ..
    opset -d on -r off -t off -l off -s off -u off $arg1
endif
