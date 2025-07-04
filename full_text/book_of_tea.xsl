<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="tei"> <xsl:template match="/tei:TEI">
    
        <html>
            <head>
                <title><xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/></title>
                <style>
                    body { font-family: sans-serif; line-height: 1.6; margin: 20px; }
                    h1 { color: #333; }
                    h2 { color: #555; }
                    h3 { color: #777; border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-top: 30px; }
                    .chapter { margin-bottom: 20px; }
                    .author-info { font-style: italic; margin-bottom: 20px; display: block;}
                    .bibl-info { margin-left: 20px; font-size: 0.9em; color: #666; }
                    .bibl-info p { margin: 5px 0; }
                    .meta-info { font-size: 0.8em; color: #888; margin-bottom: 15px;}
                    .metadata-section { border: 1px solid #eee; padding: 10px; margin-bottom: 20px; background-color: #f9f9f9; }
                    .person-name, .place-name, .term-concept { font-weight: bold; color: #007bff; }
                    .activity { font-style: italic; color: #28a745; }
                    .note { font-size: 0.85em; color: #888; margin-left: 15px; border-left: 2px solid #ddd; padding-left: 5px; }
                    .list-people { margin-top: 15px; }
                    .list-people .person { margin-bottom: 5px; }
                    .list-people .person-details { margin-left: 15px; font-size: 0.9em; color: #555; }
                    .list-people .person-details .occupation { font-style: italic; }
                    .list-places .place { margin-bottom: 5px; }
                    .list-places .place-details { margin-left: 15px; font-size: 0.9em; color: #555; }
                    .keywords-list { list-style: none; padding: 0; display: flex; flex-wrap: wrap;}
                    .keywords-list li { background-color: #e2f0fd; border-radius: 3px; padding: 3px 8px; margin: 0 5px 5px 0; font-size: 0.85em; }
                </style>
            </head>
            <body>
                <h1><xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/></h1>
                <span class="author-info">By:
                    <xsl:for-each select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author/tei:persName">
                        <xsl:value-of select="tei:forename"/> <xsl:value-of select="tei:surname"/>
                        <xsl:if test="position() &lt; last()"> and </xsl:if>
                    </xsl:for-each>
                </span>

                <div class="metadata-section">
                    <h2>Edition Information</h2>
                    <p>Edition: <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:editionStmt/tei:edition"/> (<xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:editionStmt/tei:edition/tei:date/@when"/>)</p>
                    <p>Compiled by: <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:respStmt/tei:name/tei:persName/tei:forename"/> <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:respStmt/tei:name/tei:persName/tei:surname"/></p>
                    <p>Annotations by: <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:editionStmt/tei:respStmt/tei:name/tei:persName/tei:forename"/> <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:editionStmt/tei:respStmt/tei:name/tei:persName/tei:surname"/></p>
                    <p class="meta-info">File Size: <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:extent/tei:measure[@unit='KB']"/> (<xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:extent/tei:measure[@unit='lines']"/> lines)</p>
                    <p class="meta-info">Publisher: <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:publisher"/>, <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:pubPlace/tei:placeName"/> (<xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:date/@when"/>)</p>
                    <p class="meta-info">Availability: <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:availability/tei:p"/> (<a href="{tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:availability/tei:licence/@target}" target="_blank"><xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:availability/tei:licence"/></a>)</p>

                    <h3>Notes on Edition</h3>
                    <xsl:for-each select="tei:teiHeader/tei:fileDesc/tei:notesStmt/tei:note">
                        <p class="note"><xsl:apply-templates/></p>
                    </xsl:for-each>

                    <h3>Source Descriptions</h3>
                    <xsl:for-each select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl">
                        <div class="bibl-info">
                            <h4><xsl:value-of select="tei:title[@type='main'] | tei:title[@type='digital']"/></h4>
                            <xsl:if test="tei:author">
                                <p>Author: <xsl:value-of select="tei:author/tei:persName/tei:forename"/> <xsl:value-of select="tei:author/tei:persName/tei:surname"/></p>
                            </xsl:if>
                            <xsl:if test="tei:editor">
                                <p>Editor(s): <xsl:for-each select="tei:editor">
                                    <xsl:value-of select="tei:persName/tei:forename"/> <xsl:value-of select="tei:persName/tei:surname"/>
                                    <xsl:if test="position() &lt; last()">, </xsl:if>
                                </xsl:for-each></p>
                            </xsl:if>
                            <xsl:if test="tei:publisher">
                                <p>Publisher: <xsl:value-of select="tei:publisher"/><xsl:if test="tei:pubPlace">, <xsl:value-of select="tei:pubPlace"/></xsl:if></p>
                            </xsl:if>
                            <xsl:if test="tei:date/@when or tei:date[@type='publication']/@when">
                                <p>Publication Date: <xsl:value-of select="tei:date/@when | tei:date[@type='publication']/@when"/></p>
                            </xsl:if>
                            <xsl:if test="tei:extent">
                                <p>Extent: <xsl:value-of select="tei:extent"/></p>
                            </xsl:if>
                            <xsl:if test="tei:ref">
                                <p><a href="{tei:ref/@target}" target="_blank"><xsl:value-of select="tei:ref"/></a></p>
                            </xsl:if>
                            <xsl:for-each select="tei:note">
                                <p class="note"><xsl:apply-templates/></p>
                            </xsl:for-each>
                            <xsl:if test="tei:citedRange">
                                <p>Cited Pages:
                                    <xsl:for-each select="tei:citedRange">
                                        <xsl:value-of select="."/>
                                        <xsl:if test="position() &lt; last()"> and </xsl:if>
                                    </xsl:for-each>
                                </p>
                            </xsl:if>
                        </div>
                    </xsl:for-each>
                </div>

                <div class="metadata-section">
                    <h2>Project Description</h2>
                    <p><xsl:value-of select="tei:teiHeader/tei:encodingDesc/tei:projectDesc/tei:p"/></p>

                    <h3>Languages Used</h3>
                    <ul>
                        <xsl:for-each select="tei:teiHeader/tei:profileDesc/tei:langUsage/tei:language">
                            <li><xsl:value-of select="."/> (<xsl:value-of select="@ident"/>)</li>
                        </xsl:for-each>
                    </ul>

                    <h3>Contributors and Mentions</h3>
                    <h4>Contributors</h4>
                    <ul class="list-people">
                        <xsl:for-each select="tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson[@type='contributors']/tei:person">
                            <li class="person">
                                <xsl:value-of select="tei:persName"/>
                                <xsl:if test="@source"> (<a href="{@source}" target="_blank">Source</a>)</xsl:if>
                                <div class="person-details">
                                    <span class="occupation"><xsl:value-of select="tei:occupation"/></span>
                                </div>
                            </li>
                        </xsl:for-each>
                    </ul>
                    <h4>Mentions</h4>
                    <ul class="list-people">
                        <xsl:for-each select="tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson[@type='mentions']/tei:person">
                            <li class="person">
                                <span class="person-name"><xsl:value-of select="tei:persName"/></span>
                                <xsl:if test="tei:note"><p class="note"><xsl:apply-templates select="tei:note"/></p></xsl:if>
                            </li>
                        </xsl:for-each>
                    </ul>

                    <h3>Places Mentioned</h3>
                    <ul class="list-places">
                        <xsl:for-each select="tei:teiHeader/tei:profileDesc/tei:settingDesc/tei:listPlace/tei:place">
                            <li class="place">
                                <span class="place-name"><xsl:value-of select="tei:placeName"/></span>
                                <xsl:if test="tei:idno[@type='geonames']"> (<a href="{tei:idno[@type='geonames']}" target="_blank">GeoNames</a>)</xsl:if>
                            </li>
                        </xsl:for-each>
                    </ul>

                    <h3>Keywords / Concepts</h3>
                    <p>LCSH: <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:textClass/tei:classCode[@scheme='LCSH']"/></p>
                    <ul class="keywords-list">
                        <xsl:for-each select="tei:teiHeader/tei:profileDesc/tei:textClass/tei:keywords/tei:term">
                            <li><xsl:value-of select="."/></li>
                        </xsl:for-each>
                    </ul>
                </div>

                <h2>Text Content</h2>
                <xsl:apply-templates select="tei:text/tei:body"/>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="tei:div[@type='chapter']">
        <div class="chapter">
            <h3>
                <xsl:value-of select="tei:head[@type='main']"/>
                <xsl:if test="tei:head[not(@type='main')]">
                    <xsl:text> </xsl:text>
                    <xsl:value-of select="tei:head[not(@type='main')]"/>
                </xsl:if>
            </h3>
            <xsl:apply-templates select="tei:div[@type='paragraph'] | tei:p"/>
        </div>
    </xsl:template>

    <xsl:template match="tei:div[@type='paragraph']/tei:p | tei:p">
        <p><xsl:apply-templates/></p>
    </xsl:template>

    <xsl:template match="tei:pb">
        <br/><span style="font-size: 0.8em; color: #bbb;">[Page <xsl:value-of select="@n"/>]</span><br/>
    </xsl:template>

    <xsl:template match="tei:hi">
        <xsl:choose>
            <xsl:when test="@rend='italic'">
                <i><xsl:apply-templates/></i>
            </xsl:when>
            <xsl:when test="@rend='bold'">
                <b><xsl:apply-templates/></b>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates/> </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="tei:q">
        <q><xsl:apply-templates/></q>
    </xsl:template>

    <xsl:template match="tei:lg">
        <div style="margin-left: 40px; font-style: italic;">
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="tei:l">
        <p style="margin: 0;"><xsl:apply-templates/></p>
    </xsl:template>

    <xsl:template match="tei:persName">
        <span class="person-name"><xsl:apply-templates/></span>
    </xsl:template>

    <xsl:template match="tei:placeName">
        <span class="place-name">
            <xsl:if test="@ref">
                <a href="{@ref}" target="_blank"><xsl:apply-templates/></a>
            </xsl:if>
            <xsl:if test="not(@ref)">
                <xsl:apply-templates/>
            </xsl:if>
        </span>
    </xsl:template>

    <xsl:template match="tei:term">
        <xsl:choose>
            <xsl:when test="@type='concept'">
                <span class="term-concept"><xsl:apply-templates/></span>
            </xsl:when>
            <xsl:when test="@type='activity'">
                <span class="activity"><xsl:apply-templates/></span>
            </xsl:when>
            <xsl:otherwise>
                <span class="term-default"><xsl:apply-templates/></span>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="tei:date">
        <span class="date">
            <xsl:if test="@when">
                <xsl:value-of select="@when"/>
            </xsl:if>
            <xsl:if test="@from and @to and @type='century'">
                <xsl:value-of select="@from"/>-<xsl:value-of select="@to"/> <xsl:value-of select="@type"/>
            </xsl:if>
            <xsl:if test="not(@when) and not(@from) and not(@to)">
                <xsl:apply-templates/>
            </xsl:if>
        </span>
    </xsl:template>

    <xsl:template match="tei:rs">
        <span class="reference-string">
            <xsl:if test="@type='mythicalPlace'">
                <span style="font-style: italic; color: #a0522d;"><xsl:apply-templates/></span>
            </xsl:if>
            <xsl:if test="not(@type)">
                <xsl:apply-templates/>
            </xsl:if>
        </span>
    </xsl:template>

    <xsl:template match="tei:note">
        <span class="note"> (<xsl:apply-templates/>)</span>
    </xsl:template>

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

</xsl:stylesheet>