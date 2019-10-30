<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Description</key>
	<string>Downloads latest Wacom Intuos driver installer and imports into Filewave</string>
	<key>Identifier</key>
	<string>com.github.nielshojen.filewave.pkg.WacomInkspace</string>
	<key>Input</key>
	<dict>
		<key>NAME</key>
		<string>Wacom Inkspace</string>
		<key>fw_app_bundle_id</key>
		<string>com.github.nielshojen.filewave.pkg.WacomInkspace</string>
	</dict>
	<key>MinimumVersion</key>
	<string>0.4.0</string>
	<key>ParentRecipe</key>
	<string>com.github.nielshojen.pkf.WacomInkspace</string>
	<key>Process</key>
	<array>
		<dict>
			<key>Arguments</key>
			<dict>
				<key>fw_app_bundle_id</key>
				<string>%fw_app_bundle_id%</string>
				<key>fw_app_version</key>
				<string>%version%</string>
				<key>fw_fileset_name</key>
				<string>%NAME% - %version%</string>
				<key>fw_import_source</key>
				<string>%pkg_path%</string>
			</dict>
			<key>Processor</key>
			<string>com.github.autopkg.filewave.FWTool/FileWaveImporter</string>
		</dict>
	</array>
</dict>
</plist>
