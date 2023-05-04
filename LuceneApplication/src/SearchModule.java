 import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Paths;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

import com.opencsv.CSVReader;

import org.apache.lucene.store.ByteBuffersDirectory;
import java.util.Scanner;  



public class SearchModule {
	public static void main(String[] args) throws IOException, ParseException {
		StandardAnalyzer analyzer = new StandardAnalyzer();
    	String querystr = args.length > 0 ? args[0] : "abba";
		String field = "lyrics";
		if (args.length == 2) {
			field = args[1];
			
		}
	
		Query q = new QueryParser(field, analyzer).parse(querystr);
		
		// 3. search
		int hitsPerPage = 10;
		IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get("/SearchEngine/NewIndex")));
		IndexSearcher searcher = new IndexSearcher(reader);
		
		
//		int hitsPerPage = 10;
		int pageNumber = 1;
		if (args.length == 3) {
		    pageNumber = Integer.parseInt(args[2]);
		} 
	    // Create a TopDocsCollector to retrieve the top hits
	    TopScoreDocCollector collector = TopScoreDocCollector.create(hitsPerPage * pageNumber, Integer.MAX_VALUE);
		// Execute the search and collect the top hits
		searcher.search(q, collector);
		// Retrieve the top hits for the current page
	    ScoreDoc[] hits = collector.topDocs((pageNumber - 1) * hitsPerPage, hitsPerPage).scoreDocs;
	    
		// 4. display results
		System.out.println("Found " + hits.length + " hits.");
		for(int i=0;i<hits.length;++i) {
		    int docId = hits[i].doc;
		    Document d = searcher.doc(docId);
		    System.out.println("###"+(i + 1) + "$$$" + d.get("artist") + "$$$" + d.get("title")+ "$$$" + d.get("lyrics"));		
		}  	
		
		reader.close();
	}		
}