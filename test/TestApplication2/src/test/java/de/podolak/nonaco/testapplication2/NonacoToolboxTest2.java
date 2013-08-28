package de.podolak.nonaco.testapplication2;

import org.junit.Test;

/**
 * Unit test for simple App.
 */
public class NonacoToolboxTest2 extends ChromeNonaceToolboxTest {

    @Test
    public void testNavigationNachrichten() {
        getAnchorByText("Nachrichten").click();
        
//        String content = getHtmlById("content");
//        System.out.println(content);
        
        System.out.println(driver.getPageSource());
    }
    
}