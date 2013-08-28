package de.podolak.nonaco.testapplication2;

import org.junit.Ignore;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.htmlunit.HtmlUnitDriver;

/**
 * Unit test for simple App.
 */
public class NonacoToolboxTest_Project extends NonacoToolboxTest {

    @Test
    public void testKomplettuebersicht() {
        getAnchorByText("Toolbox").click();
    }
    
}
