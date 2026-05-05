# Sysinternals Windows Group Policy Templates

Administrative Templates (ADMX/ADM) for managing Microsoft Windows Sysinternals tools via Group Policy.

These templates allow administrators to centrally configure and control Sysinternals utilities across Windows environments using standard Group Policy mechanisms.

# Purpose

Provide ADMX/ADM files that enable centralized configuration and management of Sysinternals tools through Group Policy.

# Key Features

Centralized Management

Configure Sysinternals utilities per-machine or per-user using Group Policy.

Broad Coverage

Templates currently cover 68 Sysinternals tools (see partial list below).

# Version

0.1 — includes an initial license-agreement approval policy.

Visual Assets

Screenshots or visual references are included in the repository.

Included Tools (Partial List)

AccessChk · AccessEnum · AutoRuns · BGInfo · Coreinfo · DebugView · Desktops · Disk2Vhd · Handle · Insight for Active Directory · Process Explorer · Process Monitor · PsExec · PsService · RamMap · RootkitRevealer · SDelete · Sigcheck · TCPView · VMMap · Winobj · ZoomIt

The full list of supported tools is available in the repository.

# Usage

Import the ADMX and ADML files into your Group Policy Central Store or local policy editor

Configure Sysinternals settings using Group Policy Management

Apply policies at the computer or user level as required

# Recommendations / Next Steps

Add per-tool configuration examples and recommended default values

Expand testing across multiple Windows versions and document supported OS builds

Implement automated CI to validate ADMX syntax and sample GPO exports

# Contributing

To contribute:

Open a pull request with the updated ADMX/ADML files

Include a short changelog

Provide any test results for supported Windows builds
