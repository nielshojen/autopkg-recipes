<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Description</key>
	<string>Downloads latest version of Outlook365 updater and imports into FileWave.</string>
	<key>Identifier</key>
	<string>com.github.nielshojen.filewave.pkg.Outlook365</string>
	<key>MinimumVersion</key>
	<string>0.6.1</string>
	<key>ParentRecipe</key>
	<string>com.github.autopkg.download.Outlook365</string>
	<key>Input</key>
	<dict>
		<key>NAME</key>
		<string>Microsoft Outlook 365</string>
		<key>fw_app_bundle_id</key>
		<string>com.github.rtrouton.pkg.microsoftoutlook365</string>
	</dict>
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
				<string>%pathname%</string>
			</dict>
			<key>Processor</key>
			<string>com.github.autopkg.filewave.FWTool/FileWaveImporter</string>
		</dict>
	</array>
</dict>
</plist>
