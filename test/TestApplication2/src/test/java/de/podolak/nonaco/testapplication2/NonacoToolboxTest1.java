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
public class NonacoToolboxTest1 extends NonacoToolboxTest {

    @Test
    @Ignore
    public void testLogin() {
        // do everything by hand
        WebDriver d = new HtmlUnitDriver();
        d.get(URL);
        d.findElement(By.xpath("//a[text()='Login']")).click();
        d.findElement(By.xpath("//form")).submit();
        d.findElement(By.xpath("//*[contains(.,'Willkommen.')]"));
    }
    
    @Test
    @Ignore
    public void testNavigationTop() {
        // I think this to exactly tests on HTML code, try something different ...
        /*
        WebElement navigationDiv = driver.findElement(By.id("top-navigation"));
        checkXPath(navigationDiv, "//div[@class='container']//div[@class='navbar-header']//a[@class='navbar-brand' and text()='Toolbox']");
        checkXPath(navigationDiv, "//div[@class='container']//div[@class='collapse navbar-collapse']//ul//li//a[text()='Home']");
        checkXPath(navigationDiv, "//div[@class='container']//div[@class='collapse navbar-collapse']//ul//li//a[text()='About']");
        checkXPath(navigationDiv, "//div[@class='container']//div[@class='collapse navbar-collapse']//ul//li//a[text()='Contact']");
        checkXPath(navigationDiv, "//div[@class='container']//div[@class='collapse navbar-collapse']//p[contains(text(),'Logged in as')]");
        */

        assertElementContainsText("top-navigation", "Toolbox");
        assertElementContainsText("top-navigation", "Home");
        assertElementContainsText("top-navigation", "About");
        assertElementContainsText("top-navigation", "Contact");
        assertElementContainsText("top-navigation", "Logged in as");
    }
    
    @Test
    @Ignore
    public void testNavigationLeft() {
        WebElement navigationDiv = driver.findElement(By.id("main-navigation"));

        checkXPath(navigationDiv, "//ul//li[@class='nav-header' and text()='Allgemeines']");
        checkXPath(navigationDiv, "//ul//li//a[@data-url='postings' and text()='Nachrichten']");
        checkXPath(navigationDiv, "//ul//li//a[@data-url='calendar' and text()='Kalender']");
        checkXPath(navigationDiv, "//ul//li//a[@data-url='team' and text()='Team']");
        checkXPath(navigationDiv, "//ul//li//a[@data-url='links' and text()='Links']");
        
        checkXPath(navigationDiv, "//ul//li[@class='nav-header' and text()='Projekte']");
        checkXPath(navigationDiv, "//ul//li//a[@data-url='postings' and text()='Nachrichten']");
        
        // at least the Toolbox project should be there
        checkXPath(navigationDiv, "//ul//li//a[@data-url='project/overview?urlsafe=' and " +
                                  "@data-navigation-url='project/navigation?urlsafe=' and " +
                                  "@data-urlsafe and " +
                                  "text()='Toolbox']");
    }
    
    @Test
    @Ignore
    public void testNavigationRight() {
        WebElement navigationDiv = driver.findElement(By.id("team-navigation"));

        checkXPath(navigationDiv, "//ul//li[@class='nav-header' and text()='Team']");
        checkXPath(navigationDiv, "//ul//li//a[text()='Björn']");
        checkXPath(navigationDiv, "//ul//li//a[text()='Christian']");
        checkXPath(navigationDiv, "//ul//li//a[text()='Dirk']");
        checkXPath(navigationDiv, "//ul//li//a[text()='Franziska']");
        checkXPath(navigationDiv, "//ul//li//a[text()='Lars']");
        checkXPath(navigationDiv, "//ul//li//a[text()='Marcel']");
        checkXPath(navigationDiv, "//ul//li//a[text()='Nadia']");
        checkXPath(navigationDiv, "//ul//li//a[text()='Reinhold']");
        checkXPath(navigationDiv, "//ul//li//a[text()='Robert']");
        checkXPath(navigationDiv, "//ul//li//a[text()='Stefan']");
        checkXPath(navigationDiv, "//ul//li//a[text()='Tobias']");
    }
}
