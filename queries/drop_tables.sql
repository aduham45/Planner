USE [Planner]
GO
ALTER TABLE [dbo].[place] DROP CONSTRAINT [FK__place__city_id__3CF40B7E]
GO
ALTER TABLE [dbo].[param] DROP CONSTRAINT [FK__param__cityDep_i__39237A9A]
GO
ALTER TABLE [dbo].[param] DROP CONSTRAINT [FK__param__cityArr_i__3A179ED3]
GO
/****** Object:  Table [dbo].[type]    Script Date: 23/04/2018 12:03:35 ******/
DROP TABLE [dbo].[type]
GO
/****** Object:  Table [dbo].[placeTypes]    Script Date: 23/04/2018 12:03:35 ******/
DROP TABLE [dbo].[placeTypes]
GO
/****** Object:  Table [dbo].[place]    Script Date: 23/04/2018 12:03:36 ******/
DROP TABLE [dbo].[place]
GO
/****** Object:  Table [dbo].[param]    Script Date: 23/04/2018 12:03:36 ******/
DROP TABLE [dbo].[param]
GO
/****** Object:  Table [dbo].[city]    Script Date: 23/04/2018 12:03:36 ******/
DROP TABLE [dbo].[city]
GO
